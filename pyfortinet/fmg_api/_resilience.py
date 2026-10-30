"""Shared transport policy, using pyresilience for sync and async retries."""

import asyncio
import math
from typing import TYPE_CHECKING, Any

import requests
from pyresilience import RetryConfig, resilient

from pyfortinet.exceptions import FMGHTTPException, FMGUnhandledException
from pyfortinet.settings import FMGSettings

if TYPE_CHECKING:
    import aiohttp

RETRYABLE_HTTP_STATUSES = frozenset({429, 500, 502, 503, 504})


class _TransientHTTPError(FMGHTTPException):
    """An HTTP response eligible for retry when the JSON-RPC operation is a read."""


def timeout_seconds(value: float) -> float:
    """Validate temporary timeout overrides as well as configured values."""
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError("timeout must be a finite number greater than zero")
    return value


def _retry_config(
    settings: FMGSettings,
    request: dict[str, Any],
    retry_on: tuple[type[Exception], ...],
    ignore_on: tuple[type[Exception], ...],
) -> RetryConfig:
    """Apply the same retry eligibility, attempt count, and backoff in both clients."""
    return RetryConfig(
        max_attempts=settings.retry_attempts if request.get("method") == "get" else 1,
        delay=settings.retry_delay,
        backoff_factor=settings.retry_backoff,
        max_delay=settings.retry_max_delay,
        jitter=settings.retry_jitter,
        retry_on=(_TransientHTTPError, *retry_on),
        ignore_on=ignore_on,
    )


def _check_status(status: int) -> None:
    if status in RETRYABLE_HTTP_STATUSES:
        raise _TransientHTTPError(status)
    if status >= 400:  # noqa: PLR2004 - HTTP error status range
        raise FMGHTTPException(status)


def request_json(session: requests.Session, settings: FMGSettings, request: dict[str, Any]) -> Any:
    """Send and decode a sync request, releasing each response before any retry."""
    retry = _retry_config(
        settings, request, (requests.ConnectionError, requests.Timeout), (requests.exceptions.SSLError,)
    )
    seconds = timeout_seconds(settings.timeout)

    @resilient(retry=retry)
    def attempt():
        response = session.post(str(settings.base_url), json=request, verify=settings.verify, timeout=seconds)
        try:
            _check_status(response.status_code)
            try:
                return response.json()
            except ValueError as err:
                raise FMGUnhandledException("Invalid JSON-RPC response: expected JSON") from err
        finally:
            response.close()

    return attempt()


async def async_request_json(session: "aiohttp.ClientSession", settings: FMGSettings, request: dict[str, Any]) -> Any:
    """Send and decode an async request with the same native I/O timeout policy."""
    import aiohttp  # noqa: PLC0415 - optional async dependency

    retry = _retry_config(
        settings, request, (aiohttp.ClientConnectionError, asyncio.TimeoutError), (aiohttp.ClientSSLError,)
    )
    seconds = timeout_seconds(settings.timeout)
    timeout = aiohttp.ClientTimeout(total=None, connect=seconds, sock_connect=seconds, sock_read=seconds)

    @resilient(retry=retry)
    async def attempt():
        response = await session.post(str(settings.base_url), json=request, ssl=settings.verify, timeout=timeout)
        try:
            _check_status(response.status)
            try:
                return await response.json()
            except (ValueError, aiohttp.ContentTypeError) as err:
                raise FMGUnhandledException("Invalid JSON-RPC response: expected JSON") from err
        finally:
            response.release()

    return await attempt()
