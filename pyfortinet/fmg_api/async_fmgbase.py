"""Async FMGBase connection"""

import asyncio
import functools
import logging
import re
import time
from contextlib import contextmanager
from copy import copy
from random import randint
from typing import Any, Callable, Optional, Union, List, Coroutine
from dataclasses import dataclass

from pyfortinet.fmg_api.fmgbase import FMGResponse

try:
    import aiohttp
except ModuleNotFoundError:
    """async install option"""

from pydantic import SecretStr

from pyfortinet.exceptions import (
    FMGException,
    FMGAuthenticationException,
    FMGTokenException,
    FMGLockNeededException,
    FMGLockException,
    FMGUnhandledException, FMGObjectNotExistException,
)
from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.task import Task
from pyfortinet.settings import FMGSettings
from pyfortinet.fmg_api.error_table import get_fmg_error

logger = logging.getLogger(__name__)


def auth_required(func: Callable) -> Callable:
    """Decorator to provide authentication for the method

    Args:
        func: function to handle authentication errors

    Returns:
        (Callable): function with authentication handling enabled
    """

    @functools.wraps(func)
    async def auth_decorated(self: Union[dict, "AsyncFMGBase"] = None, *args, **kwargs):
        """method which needs authentication"""
        if not self._token:
            raise FMGTokenException("No token was obtained. Open connection first!")
        try:
            return await func(self, *args, **kwargs)
        except FMGAuthenticationException as err:
            try:  # try again after refreshing token
                self._token = await self._get_token()  # pylint: disable=protected-access  # decorator of methods
                return await func(self, *args, **kwargs)
            except FMGException as err2:
                raise err2 from err

    return auth_decorated


def error_handling(func: Callable) -> Callable:
    """Decorator to provide error handling for the methods"""
    @functools.wraps(func)
    async def error_decorated(self: "AsyncFMGBase", *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except FMGException as err:
            if self.raise_on_error:
                raise
            result = AsyncFMGResponse(data=[{"error": str(err)}], success=False)
            return result

    return error_decorated

def lock(func: Callable) -> Callable:
    """Decorator to provide ADOM locking if needed

    Args:
        func: function to handle errors complaining about no locking

    Returns:
        (Callable): function with lock handling enabled
    """

    @functools.wraps(func)
    async def lock_decorated(self: "AsyncFMGBase" = None, *args, **kwargs):
        """method which needs locking"""
        try:
            return await func(self, *args, **kwargs)
        except (FMGLockNeededException, FMGAuthenticationException) as err:
            try:  # try again after locking
                if not args:  # in case we got kwargs request
                    args = [kwargs.get("request")]
                    del kwargs["request"]
                # ensure args[0] is a list of request dict or obj to support multiple request in one API call
                if isinstance(args[0], list):
                    args_to_check = args[0]
                else:
                    args_to_check = [args[0]]
                for arg in args_to_check:
                    if isinstance(arg, dict):
                        url = arg.get("url")
                        adom_match = re.search(r"^(?:/\w+){,3}/(?P<adom>global\b|(?<=adom/)[\w-]+)/?", url)
                        if adom_match:
                            adom = adom_match.group("adom")
                        elif self.adom:
                            adom = self.adom
                        else:
                            raise FMGException(f"No ADOM found to lock in url '{url}'") from err
                    elif isinstance(arg, FMGObject):
                        adom = arg.fmg_scope
                    else:
                        raise ValueError(f"Unknown request: {arg}")
                    if adom not in self.lock.locked_adoms:
                        await self.lock(adom)
                    # else:  # ADOM already locked, do not try to lock it again
                    #     raise
                return await func(self, *args, **kwargs)
            except FMGException as err2:
                raise err2 from err

    return lock_decorated


@dataclass
class AsyncFMGResponse(FMGResponse):
    """Response to a request

    Attributes:
        data (dict|List[FMGObject]): response data
        success (bool): True on success
        fmg (AsyncFMGBase): FMG object tied to this response
    """

    fmg: "AsyncFMGBase" = None

    async def wait_for_task(
        self, callback: Callable[[int, str], Optional[Coroutine]] = None, timeout: int = 60, loop_interval: int = 2
    ):
        if not self.success or not self.fmg:
            return
        return await self.fmg.wait_for_task(self, callback=callback, timeout=timeout, loop_interval=loop_interval)


class AsyncFMGLockContext:
    """Lock FMG workspace"""

    def __init__(self, fmg: "AsyncFMGBase"):
        self._fmg = fmg
        self._locked_adoms = set()
        self._uses_workspace = None
        self._uses_adoms = None

    @property
    def uses_workspace(self) -> bool:
        """returns workspace usage"""
        return self._uses_workspace

    @property
    def locked_adoms(self) -> set[str]:
        """returns locked adom set"""
        return self._locked_adoms

    async def __call__(self, *adoms: str):
        await self.check_mode()
        if self._uses_workspace:
            await self.lock_adoms(*adoms)
        return self

    async def check_mode(self):
        """Get workspace-mode from config"""
        url = "/cli/global/system/global"
        result = await self._fmg.get({"url": url, "fields": ["workspace-mode", "adom-status"]})
        self._uses_workspace = result.data[0]["data"].get("workspace-mode") != 0
        # self.uses_adoms = result.data["data"].get("adom-status") == 1

    async def lock_adoms(self, *adoms: str) -> AsyncFMGResponse:
        """Lock adom list

        If no adom specified, global workspace will be locked

        Args:
            *adoms (str): list of adom names

        Returns:
            Response object
        """
        result = AsyncFMGResponse(fmg=self._fmg)
        if not adoms:
            adoms = ["root"]
        for adom in adoms:
            url = "/dvmdb/global/workspace/lock/" if adom.lower() == "global" else f"/dvmdb/adom/{adom}/workspace/lock/"
            result.data = [{adom: await self._fmg.exec(request={"url": url})}]
            if result.data[0][adom].data[0].get("error"):
                raise FMGLockException(result.data[0][adom].data[0])
            self._locked_adoms.add(adom)
        return result

    async def unlock_adoms(self, *adoms) -> AsyncFMGResponse:
        """unlock ADOMs"""
        result = AsyncFMGResponse(fmg=self._fmg)
        if not adoms:
            adoms = copy(self._locked_adoms)
        for adom in adoms:
            if adom.lower() == "global":
                url = "/dvmdb/global/workspace/unlock/"
            else:
                url = f"/dvmdb/adom/{adom}/workspace/unlock/"
            result.data = [{adom: await self._fmg.exec(request={"url": url})}]
            if not result.data[0][adom].data[0].get("error"):
                self._locked_adoms.remove(adom)

        if self._locked_adoms:
            raise FMGException(f"Failed to unlock ADOMs: {self._locked_adoms}")
        return result

    async def commit_changes(self, adoms: Optional[list] = None, aux: bool = False) -> list[AsyncFMGResponse]:
        """Apply workspace changes in the DB

        Args:
            adoms: list of ADOMs to commit. If empty, commit ALL ADOMs.
            aux:

        Returns:
            (list[FMGResponse]): List of response of operations
        """
        results = []
        if not adoms:
            adoms = self._locked_adoms
        for adom in adoms:
            if aux:
                url = f"/pm/config/adom/{adom}/workspace/commit"
            elif adom.lower() == "global":
                url = "/dvmdb/global/workspace/commit/"
            else:
                url = f"/dvmdb/adom/{adom}/workspace/commit"
            results.append(await self._fmg.exec({"url": url}))
        return results


class AsyncFMGBase:
    """Fortimanager connection class

    This can be used as a connection handler for the FortiManager. It maintains state of operation and provides
    functions to communicate with the FMG.

    Attributes:
        lock (AsyncFMGLockContext): Workspace lock handler

    Examples:
        Possible arguments to initialize: [FMGSettings](../settings.md#settings.FMGSettings)

        ### Using as context manager
        ```pycon

        >>> import asyncio
        >>> settings = {...}
        >>> async def get_version(**settings):
        ...     async with AsyncFMGBase(**settings) as conn:
        ...         print(await conn.get_version())
        >>> asyncio.run(get_version())
        ```

        ### Using as function:
        ```pycon

        >>> import asyncio
        >>> from pyfortinet.exceptions import FMGException
        >>> settings = {...}
        >>> async def get_version(**settings):
        ...     conn = AsyncFMGBase(**settings)
        ...     try:
        ...         await conn.open()
        ...         print(await conn.get_version())
        ...     except FMGException as err:
        ...         print(f"Error: {err}")
        ...     finally:
        ...         await conn.close()
        >>> asyncio.run(get_version())
        ```
    """

    def __init__(self, settings: Optional[FMGSettings] = None, **kwargs):
        """Initializes FMGBase

        Args:
            settings (Settings): FortiManager settings

        Keyword Args:
            base_url (str): Base URL to access FMG (e.g.: https://myfmg)
            username (str): User to authenticate
            password (str): Password for authentication
            adom (str): ADOM to use for this connection
            verify (bool): Verify SSL certificate (REQUESTS_CA_BUNDLE can set accepted CA cert)
            timeout (float): Connection timeout for requests in seconds
            raise_on_error (bool): Raise exception on error
            discard_on_close (bool): Discard changes after connection close (workspace mode)
            discard_on_error (bool): Discard changes when exception occurs (workspace mode)
        """
        try:
            import aiohttp
        except ModuleNotFoundError:
            raise Exception("Please install aiohttp or pip install pyfortinet[async]!")
        if not settings:
            settings = FMGSettings(**kwargs)
        self._settings = settings
        self._token: Optional[SecretStr] = None
        self._session: Optional[aiohttp.ClientSession] = None
        self.lock = AsyncFMGLockContext(self)
        self._raise_on_error: bool = settings.raise_on_error
        self._id: int = randint(1, 256)  # pick a random id for this session (check logs for a particular session)

    @property
    def adom(self) -> str:
        """Returns current selected adom"""
        return self._settings.adom

    @adom.setter
    def adom(self, adom: str) -> None:
        self._settings.adom = adom

    @property
    def discard_on_close(self) -> bool:
        """Returns discard_on_close value"""
        return self._settings.discard_on_close

    @discard_on_close.setter
    def discard_on_close(self, setting: bool) -> None:
        self._settings.discard_on_close = bool(setting)

    @property
    def raise_on_error(self):
        """Returns raise_on_error value"""
        return self._raise_on_error

    @raise_on_error.setter
    def raise_on_error(self, value: bool):
        self._raise_on_error = bool(value)

    @contextmanager
    async def lock_adom(self, adom: Optional[str] = None, keep_locked: bool = False):
        """Locks specified ADOM explicitly

        The usual error based locking not always work. For example FMG replies authentication error while running
        a job to create new Device in device database. This makes error handling unusable and therefore this
        context manager can be used to lock ADOM for the job run duration.

        If adom was already locked, this function won't lock it again and won't unlock it either.

        Args:
            adom: ADOM to be locked as string. If not specified, currently used ADOM will be used.
            keep_locked: If True, the lock is not released after operation. (default: False)

        Yields:
            (str): adom name (not used normally)
        """
        if not adom:
            adom = self.adom
        if not adom:
            raise ValueError("ADOM must be specified!")
        if self.lock.uses_workspace is None:
            await self.lock.check_mode()
        did_lock = False
        if self.lock.uses_workspace and adom not in self.lock.locked_adoms:
            await self.lock.lock_adoms(adom)
            did_lock = True
        try:
            yield adom
        finally:
            if did_lock and not keep_locked:
                await self.lock.unlock_adoms(adom)

    async def open(self) -> "AsyncFMGBase":
        """open connection"""
        logger.debug("Initializing connection to %s with id: %s", self._settings.base_url, self._id)
        self._session = aiohttp.ClientSession()
        self._token = await self._get_token()
        return self

    async def close(self, discard_changes: bool = False):
        """close connection"""
        # Logout and expire token
        request = {
            "id": self._id,
            "method": "exec",
            "params": [{"url": "/sys/logout"}],
            "session": self._token.get_secret_value(),
        }
        self._settings.discard_on_close = self._settings.discard_on_close or discard_changes
        try:
            try:
                if self.lock.uses_workspace:
                    if not self.discard_on_close:
                        await self.lock.commit_changes()
                    await self.lock.unlock_adoms()
            except FMGException:  # go ahead and ensure logout regardless we could unlock
                pass
            req = await self._session.post(
                str(self._settings.base_url), json=request, ssl=self._settings.verify, timeout=self._settings.timeout
            )
            status = (await req.json()).get("result", [{}])[0].get("status", {})
            if status.get("code") != 0:
                logger.warning("Logout failed!")
        except aiohttp.ClientConnectorError:
            logger.warning("Logout failed!")
        finally:
            await self._session.close()
        self._token = None
        logger.debug("Closed session")

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        if exc_type is not None:
            await self.close(discard_changes=self._settings.discard_on_error or self._settings.discard_on_close)
            return
        await self.close(discard_changes=self.discard_on_close)

    async def _post(self, request: dict) -> Any:
        logger.debug("posting data: %s", request)
        req = await self._session.post(
            str(self._settings.base_url), json=request, ssl=self._settings.verify, timeout=self._settings.timeout
        )
        results = (await req.json()).get("result", [])
        for result in results:
            status = result["status"]
            if status["code"] == 0:
                continue
            error = get_fmg_error(error_code=status["code"])
            if error is not None:  # found error code
                if isinstance(error, str):  # it's a string, not handled
                    raise FMGUnhandledException(status)
                raise error(status)  # raise handled exception
            raise FMGUnhandledException(status)
        return results[0] if len(results) == 1 else results

    async def _get_token(self) -> SecretStr:
        """Get authentication token

        Raises:
            (FMGTokenException): upon problem getting the token
        """
        logger.debug("Getting token..")
        request = {
            "id": self._id,
            "method": "exec",
            "params": [
                {
                    "data": {"passwd": self._settings.password.get_secret_value(), "user": self._settings.username},
                    "url": "/sys/login/user",
                }
            ],
        }
        try:
            req = await self._session.post(str(self._settings.base_url), json=request, ssl=self._settings.verify)
            status = (await req.json()).get("result", [{}])[0].get("status", {})
            if status.get("code") != 0:
                if "No permission for resource" in status.get("message"):
                    raise FMGUnhandledException("No permission for resource, probably user does not have API access!")
                raise FMGTokenException("Login failed, wrong credentials!")
            logger.debug("Token obtained")
        except FMGTokenException as err:
            logger.error("Can't gather token: %s", err)
            raise err
        except aiohttp.ClientConnectorError as err:
            logger.error("Can't gather token: %s", err)
            raise err
        token = (await req.json()).get("session", "")
        return SecretStr(token)

    @error_handling
    @auth_required
    async def get_version(self) -> str:
        """Gather FMG version"""
        request = {
            "method": "get",
            "params": [{"url": "/sys/status"}],
            "id": 1,
            "session": self._token.get_secret_value(),
        }
        req = await self._post(request)
        return req["data"]["Version"]

    @error_handling
    @auth_required
    @lock
    async def exec(self, request: dict[str, str]) -> AsyncFMGResponse:
        """Execute on FMG

        This method currently does not support multiple requests in one call!
        """
        logger.info("requesting exec with low-level op to %s", request.get("url"))
        body = {
            "method": "exec",
            "params": [
                {
                    "data": request.get("data"),
                    "url": request.get("url"),
                }
            ],
            "session": self._token.get_secret_value(),
            "id": self._id,
        }
        api_result = await self._post(request=body)
        if isinstance(api_result, dict):
            api_result = [api_result]
        result = AsyncFMGResponse(fmg=self, data=api_result, success=api_result[0].get("status", {}).get("code") == 0)
        return result

    # noqa: PLR0912 - Too many branches
    @error_handling
    @auth_required
    async def get(self, request: dict[str, Any]) -> AsyncFMGResponse:  # noqa: PLR0912 - Too many branches
        """Get info from FMG

        This method currently does not support multiple requests in one call!

        Args:
            request: Get operation's param structure

        Examples:
            ```pycon

            >>> import asyncio
            >>> address_request = {
            ...    "url": "/pm/config/global/obj/firewall/address",
            ...    "filter": [ ["name", "==", "test-address"] ],
            ...    "fields": [ "name", "subnet" ]
            ... }
            >>> settings = {...}
            >>> async def get_address(request: dict[str, Any]):
            ...     async with AsyncFMGBase(**settings) as fmg:
            ...         return await fmg.get(address_request)
            >>> asyncio.run(get_address())
            ```

        Returns:
            (AsyncFMGResponse): response object with data
        """
        body = {
            "method": "get",
            "params": [request],
            "verbose": 1,  # get string values instead of numeric
            "session": self._token.get_secret_value(),
            "id": self._id,
        }
        result = AsyncFMGResponse(fmg=self)
        try:
            api_result = await self._post(request=body)
        except FMGObjectNotExistException:
            # handling when specific requested object doesn't exist
            # we don't error out, but give an empty list
            result.data = {"data": [], "status": {"code": 0}}
            return result

        # handling empty result list
        if not api_result.get("data"):
            result.data = {"data": [], "status": {"code": 0}}
            return result

        # processing result list
        result.data = api_result if isinstance(api_result, list) else [api_result]
        result.success = True
        # result.status = api_result.get("status", {}).get("code", 400)

        return result

    @error_handling
    @auth_required
    @lock
    async def add(self, request: Union[dict[str, Any], List[dict[str, Any]]]) -> AsyncFMGResponse:
        """Add operation

        Notes:
            Multiple requests in one call is supported

        Args:
            request: Add operation's data structure

        Examples:
            ```pycon

            >>> import asyncio
            >>> settings = {...}
            >>> address_request = {
            ...     "url": "/pm/config/global/obj/firewall/address",
            ...     "data": {
            ...         "name": "test-address",
            ...         "associated-interface": "inside",
            ...         "obj-type": "ip",
            ...         "type": "ipmask",
            ...         "start-ip": "10.0.0.1/24"
            ...     }
            ... }
            >>> async def add_request(request: dict[str,Any]):
            ...     async with AsyncFMGBase(**settings) as fmg:
            ...         return await fmg.add(address_request)
            >>> asyncio.run(add_request(address_request))
            ```

        Returns:
            (AsyncFMGResponse): Result of operation
        """
        response = AsyncFMGResponse(fmg=self)
        if isinstance(request, dict):
            request = [request]
        body = {
            "method": "add",
            "params": [
                {
                    "data": req.get("data"),
                    "url": req.get("url"),
                }
                for req in request
            ],
            "session": self._token.get_secret_value(),
            "id": self._id,
        }
        api_result = await self._post(request=body)
        if isinstance(api_result, dict):
            api_result = [api_result]
        response.success = all(result.get("status", {}).get("code") == 0 for result in api_result)
        response.data = api_result
        return response

    @error_handling
    @auth_required
    @lock
    async def update(self, request: Union[dict[str, Any], List[dict[str, Any]]]) -> AsyncFMGResponse:
        """Update operation

        Notes:
            Multiple requests in one call is supported

        Args:
            request: Update operation's data structure

        Examples:
            ```pycon

            >>> import asyncio
            >>> settings = {...}
            >>> address_request = {
            ...     "url": "/pm/config/global/obj/firewall/address",
            ...     "data": {
            ...         "name": "test-address",
            ...         "associated-interface": "inside",
            ...         "obj-type": "ip",
            ...         "type": "ipmask",
            ...         "start-ip": "10.0.0.1/24"
            ...     }
            ... }
            >>> async def update_address(request):
            ...     async with AsyncFMGBase(**settings) as fmg:
            ...         return await fmg.update(address_request)
            >>> asyncio.run(update_address())
            ```

        Returns:
            (AsyncFMGResponse): Result of operation
        """
        response = AsyncFMGResponse(fmg=self)
        if isinstance(request, dict):
            request = [request]
        body = {
            "method": "update",
            "params": [
                {
                    "data": req.get("data"),
                    "url": req.get("url"),
                }
                for req in request
            ],
            "session": self._token.get_secret_value(),
            "id": self._id,
        }
        api_result = await self._post(request=body)
        if isinstance(api_result, dict):
            api_result = [api_result]
        response.success = all(result.get("status", {}).get("code") == 0 for result in api_result)
        response.data = api_result
        return response

    @error_handling
    @auth_required
    @lock
    async def set(self, request: Union[dict[str, Any], List[dict[str, Any]]]) -> AsyncFMGResponse:
        """Set operation

        Notes:
            Multiple requests in one call is supported

        Args:
            request: Set operation's data structure

        Examples:
            ```pycon

            >>> import asyncio
            >>> settings = {...}
            >>> address_request = {
            ...     "url": "/pm/config/global/obj/firewall/address",
            ...     "data": {
            ...         "name": "test-address",
            ...         "associated-interface": "inside",
            ...         "obj-type": "ip",
            ...         "type": "ipmask",
            ...         "start-ip": "10.0.0.1/24"
            ...     }
            ... }
            >>> async def set_address(request):
            ...     async with AsyncFMGBase(**settings) as fmg:
            ...         return await fmg.set(address_request)
            >>> asyncio.run(set_address())
            ```

        Returns:
            (AsyncFMGResponse): Result of operation
        """
        response = AsyncFMGResponse(fmg=self)
        if isinstance(request, dict):
            request = [request]
        body = {
            "method": "set",
            "params": [
                {
                    "data": req.get("data"),
                    "url": req.get("url"),
                }
                for req in request
            ],
            "session": self._token.get_secret_value(),
            "id": self._id,
        }
        api_result = await self._post(request=body)
        if isinstance(api_result, dict):
            api_result = [api_result]
        response.success = all(result.get("status", {}).get("code") == 0 for result in api_result)
        response.data = api_result
        return response

    @error_handling
    @auth_required
    @lock
    async def delete(self, request: Union[dict[str, Any], List[dict[str, Any]]]) -> AsyncFMGResponse:
        """Delete operation

        Notes:
            Multiple requests in one call is supported

        Args:
            request: Update operation's data structure

        Examples:
            ```pycon

            >>> import asyncio
            >>> settings = {...}
            >>> address_request = {
            ...     "url": "/pm/config/global/obj/firewall/address/test-address",
            ... }
            >>> async def delete_address(request):
            ...     async with AsyncFMGBase(**settings) as fmg:
            ...         await fmg.delete(request)
            >>> asyncio.run(delete_address(address_request))
            ```

        Returns:
            (FMGResponse): Result of operation
        """
        response = AsyncFMGResponse(fmg=self)
        if isinstance(request, dict):
            request = [request]
        body = {
            "method": "delete",
            "params": [
                {
                    "url": req.get("url"),
                }
                for req in request
            ],
            "session": self._token.get_secret_value(),
            "id": self._id,
        }
        api_result = await self._post(request=body)
        if isinstance(api_result, dict):
            api_result = [api_result]
        response.success = all(result.get("status", {}).get("code") == 0 for result in api_result)
        response.data = api_result
        return response

    @error_handling
    @auth_required
    @lock
    async def clone(
        self, request: Union[dict[str, Any], List[dict[str, Any]]], create_task: bool = False
    ) -> AsyncFMGResponse:
        """Clone operation

        Notes:
            Multiple requests in one call is supported

        Args:
            request (dict): Clone operation's data structure
            create_task (bool): Wheter to create task

        Examples:
            ```pycon

            >>> import asyncio
            >>> settings = {...}
            >>> clone_request = {
            ...     "url": "/pm/config/global/obj/firewall/address/test-address",  # source object
            ...     "data": {
            ....         "name": "clone-address",  # destination object
            ...     }
            ... }
            >>> async def clone_address(request):
            ...     async with AsyncFMGBase(**settings) as fmg:
            ...         await fmg.clone(request)
            >>> asyncio.run(clone_address(clone_request))
            ```

        Returns:
            (FMGResponse): Result of operation
        """
        response = AsyncFMGResponse(fmg=self)
        if isinstance(request, dict):
            request = [request]
        body = {
            "method": "clone",
            "params": [
                {
                    "url": req.get("url"),
                    "data": req.get("data"),
                }
                for req in request
            ],
            "session": self._token.get_secret_value(),
            "id": self._id,
        }
        adom = self.adom if self.adom != "global" else "root"
        if create_task:
            body["create_task"] = {
                "adom": adom,
                # name task after this request object
                "name": f"cloning task of {', '.join(req.get('url').split('/')[-1] for req in request)}",
            }
        api_result = await self._post(request=body)
        if isinstance(api_result, dict):
            api_result = [api_result]
        response.success = all(result.get("status", {}).get("code") == 0 for result in api_result)
        response.data = api_result
        return response

    async def wait_for_task(
        self,
        task_res: Union[int, AsyncFMGResponse],
        callback: Union[Coroutine[Any, Any, None], Callable[[int, str], None]] = None,
        timeout: int = 60,
        loop_interval: int = 2,
    ) -> Union[str, None]:
        """Wait for task to finish

        Args:
            task_res: (int, AsyncFMGResponse): Task or task ID to check
            callback: (Callable[[int, str], None]): function to call in each iteration.
                                              It must accept 2 args which are the current percentage and latest log line
            timeout: (int): timeout for waiting in seconds
            loop_interval: (int): interval between task status updates in seconds

        Example:
            ```pycon

            >>> import asyncio
            >>> from pyfortinet.fmg_api.dvmcmd import DeviceTask
            >>> from pyfortinet.fmg_api.dvmdb import Device
            >>> from rich.progress import Progress
            >>> settings = {...}
            >>> test_device = Device(name="test", ip="1.1.1.1", adm_usr="test", adm_pass="<PASSWORD>")
            >>> async def add_device(device: Device):
            ...     async with AsyncFMGBase(**settings) as fmg:
            ...         task = DeviceTask(adom=fmg.adom, device=device)
            ...         result = await fmg.exec(task)
            ...         with Progress() as progress:
            ...             prog_task = progress.add_task(f"Adding device {device.name}", total=100)
            ...             update_progress = lambda percent, log: progress.update(prog_task, percent)
            ...             await result.wait_for_task(callback=update_progress)
            >>> asyncio.run(add_device(test_device))
            ```
        """
        task_id = task_res if isinstance(task_res, int) else task_res.data[0].get("data", {}).get("taskid")
        if task_id is None:
            return
        start_time = time.time()
        while True:
            task: Task = (await self.get(Task, F(id=task_id))).first()
            if not task:
                return
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Timed out waiting {timeout} seconds for the task {task.id}!")
            if callable(callback):
                if asyncio.iscoroutinefunction(callback):
                    await callback(task.percent, task.line[-1].detail if task.line else "")
                else:
                    callback(task.percent, task.line[-1].detail if task.line else "")
            # exit on the following states
            if task.state in ["cancelled", "done", "error", "aborted", "to_continue", "unknown"]:
                return task.state
            await asyncio.sleep(loop_interval)
