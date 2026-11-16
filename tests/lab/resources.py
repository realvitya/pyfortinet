"""Explicit ownership and compensating cleanup for live lab tests."""

from collections.abc import Callable
from typing import Any, TypeVar
from uuid import uuid4

from pyfortinet.exceptions import FMGObjectNotExistException
from pyfortinet.fmg_api import FMGObject

ObjectT = TypeVar("ObjectT", bound=FMGObject)


class LabCleanupError(AssertionError):
    """One or more compensating operations failed; the lab needs inspection."""


class _Resources:
    def __init__(self, client: Any) -> None:
        self.client = client
        self.prefix = "pf" + uuid4().hex[:6]
        self._cleanup: list[tuple[str, Callable[[], Any]]] = []
        self._reserved: set[str] = set()

    def name(self, label: str) -> str:
        """Return a stable name for this test, short enough for interface names."""
        if not label or len(label) > 6 or not label.isalnum():  # noqa: PLR2004
            raise ValueError("Use a unique alphanumeric label of at most six characters")
        return f"{self.prefix}-{label}"

    def defer(self, label: str, action: Callable[[], Any]) -> None:
        """Register compensation before an operation that might partially succeed."""
        self._cleanup.append((label, action))

    def _object(self, kind: type[ObjectT], label: str, **fields: Any) -> ObjectT:
        obj = self.client.get_obj(kind, name=self.name(label), **fields)
        obj.fmg_scope = self.client.adom
        return obj

    @staticmethod
    def _check(response: Any) -> Any:
        if not response.success:
            raise AssertionError("Lab operation returned an unsuccessful response")
        return response

    @staticmethod
    def _report(failures: list[str]) -> None:
        if failures:
            # Do not include exception messages: transport diagnostics can contain credentials.
            raise LabCleanupError("Cleanup failed; inspect remaining resources: " + ", ".join(failures))


class LabResources(_Resources):
    """Own only absent resources; never delete or overwrite a pre-existing object."""

    def exists(self, url: str) -> bool:
        try:
            result = self._check(self.client.get({"url": url}))
        except FMGObjectNotExistException:
            return False
        return bool(result.data and result.data[0].get("data"))

    def reserve(self, url: str, delete: Any = None) -> str:
        """Check absence and register idempotent cleanup before creating a resource."""
        if url in self._reserved:
            return url
        if self.exists(url):
            raise AssertionError(f"Refusing to reuse an existing lab resource: {url}")

        def cleanup() -> None:
            if self.exists(url):
                result = self._check(delete() if delete else self.client.delete({"url": url}))
                if delete:
                    result.wait_for_task()  # Device removal is a task, not a plain object delete.
                if self.exists(url):
                    raise AssertionError("Resource still exists after cleanup")

        self._reserved.add(url)
        self.defer(url, cleanup)
        return url

    def object(self, kind: type[ObjectT], label: str, **fields: Any) -> ObjectT:
        """Construct an owned object without writing it yet."""
        obj = self._object(kind, label, **fields)
        self.reserve(obj.get_url(method="delete"))
        return obj

    def wait(self, response: Any) -> None:
        """Keep a failed task wait registered for another attempt during teardown."""
        finished = False

        def finish() -> None:
            nonlocal finished
            if not finished:
                response.wait_for_task()
                finished = True

        self.defer("pending task", finish)
        finish()

    def cleanup(self) -> None:
        """Try every compensation, then report all failures without leaking secrets."""
        failures = []
        previous = self.client.raise_on_error
        self.client.raise_on_error = True
        try:
            while self._cleanup:
                label, action = self._cleanup.pop()
                try:
                    action()
                except Exception as error:  # Continue cleaning independent resources.
                    failures.append(f"{label} ({type(error).__name__})")
        finally:
            self.client.raise_on_error = previous
        self._report(failures)


class AsyncLabResources(_Resources):
    """Async equivalent; all compensation runs on the client's event loop."""

    async def exists(self, url: str) -> bool:
        try:
            result = self._check(await self.client.get({"url": url}))
        except FMGObjectNotExistException:
            return False
        return bool(result.data and result.data[0].get("data"))

    async def reserve(self, url: str, delete: Any = None) -> str:
        """Check absence and register cleanup before an awaited write."""
        if url in self._reserved:
            return url
        if await self.exists(url):
            raise AssertionError(f"Refusing to reuse an existing lab resource: {url}")

        async def cleanup() -> None:
            if await self.exists(url):
                result = self._check(await (delete() if delete else self.client.delete({"url": url})))
                if delete:
                    await result.wait_for_task()
                if await self.exists(url):
                    raise AssertionError("Resource still exists after cleanup")

        self._reserved.add(url)
        self.defer(url, cleanup)
        return url

    async def object(self, kind: type[ObjectT], label: str, **fields: Any) -> ObjectT:
        """Construct an owned object without writing it yet."""
        obj = self._object(kind, label, **fields)
        await self.reserve(obj.get_url(method="delete"))
        return obj

    async def wait(self, response: Any) -> None:
        """Keep unfinished tasks in the teardown journal."""
        finished = False

        async def finish() -> None:
            nonlocal finished
            if not finished:
                await response.wait_for_task()
                finished = True

        self.defer("pending task", finish)
        await finish()

    async def cleanup(self) -> None:
        """Await every compensation, including when an earlier cleanup fails."""
        failures = []
        previous = self.client.raise_on_error
        self.client.raise_on_error = True
        try:
            while self._cleanup:
                label, action = self._cleanup.pop()
                try:
                    await action()
                except Exception as error:
                    failures.append(f"{label} ({type(error).__name__})")
        finally:
            self.client.raise_on_error = previous
        self._report(failures)
