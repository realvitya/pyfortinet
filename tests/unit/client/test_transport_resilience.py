"""The real pyresilience policy behaves identically with both HTTP transports."""

import asyncio
import subprocess
import sys
import threading
from unittest.mock import AsyncMock, Mock

import aiohttp
import pytest
import requests
from pydantic import ValidationError

from pyfortinet import AsyncFMG, FMGSettings
from pyfortinet.exceptions import FMGHTTPException, FMGInvalidDataException, FMGUnhandledException
from tests.unit.conftest import resolve


@pytest.fixture
def transport(client):
    asynchronous = isinstance(client, AsyncFMG)
    client._settings.retry_delay = 0
    client._settings.retry_jitter = False
    client._session = Mock()
    client._session.post = AsyncMock() if asynchronous else Mock()
    client._session.close = AsyncMock() if asynchronous else Mock()

    def response(status=200, payload=None):
        result = Mock(status_code=status, status=status)
        payload = {"result": [{"status": {"code": 0}, "data": []}]} if payload is None else payload
        result.json = AsyncMock(return_value=payload) if asynchronous else Mock(return_value=payload)
        return result

    return response


def network_error(client):
    return aiohttp.ClientConnectionError if isinstance(client, AsyncFMG) else requests.ConnectionError


def released(client, response):
    return response.release if isinstance(client, AsyncFMG) else response.close


def test_read_retries_connection_failure(client, transport):
    response = transport()
    client._session.post.side_effect = [network_error(client)("disconnected"), response]
    assert resolve(client.get({"url": "/example"})).success
    assert client._session.post.call_count == 2  # noqa: PLR2004
    released(client, response).assert_called_once_with()


def test_read_exhaustion_preserves_native_exception(client, transport):
    client._settings.retry_attempts = 4
    error = network_error(client)("unavailable")
    client._session.post.side_effect = error
    with pytest.raises(type(error)) as caught:
        resolve(client.get({"url": "/example"}))
    assert caught.value is error
    assert client._session.post.call_count == client._settings.retry_attempts


@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
def test_read_retries_transient_http_status_and_releases_response(client, transport, status):
    failed, success = transport(status), transport()
    client._session.post.side_effect = [failed, success]
    assert resolve(client.get({"url": "/example"})).success
    failed.json.assert_not_called()
    released(client, failed).assert_called_once_with()
    released(client, success).assert_called_once_with()


@pytest.mark.parametrize("raise_on_error", [False, True])
def test_http_exhaustion_obeys_library_error_policy(client, transport, raise_on_error):
    client.raise_on_error = raise_on_error
    client._session.post.side_effect = [transport(503) for _ in range(client._settings.retry_attempts)]
    if raise_on_error:
        with pytest.raises(FMGHTTPException) as caught:
            resolve(client.get({"url": "/example"}))
        assert caught.value.status_code == 503  # noqa: PLR2004
    else:
        result = resolve(client.get({"url": "/example"}))
        assert not result.success
        assert "503" in result.data[0]["error"]
    assert client._session.post.call_count == client._settings.retry_attempts


@pytest.mark.parametrize("method", ["add", "set", "update", "delete", "clone", "exec"])
def test_writes_are_not_replayed_after_transport_failures(client, transport, method):
    error = network_error(client)("response lost")
    client._session.post.side_effect = error
    with pytest.raises(type(error)):
        resolve(getattr(client, method)({"url": "/example"}))
    client._session.post.assert_called_once()


@pytest.mark.parametrize("method", ["add", "exec"])
def test_transient_http_status_does_not_replay_write(client, transport, method):
    client._session.post.return_value = transport(503)
    with pytest.raises(FMGHTTPException):
        resolve(getattr(client, method)({"url": "/example"}))
    client._session.post.assert_called_once()


def test_login_is_not_replayed(client, transport):
    error = network_error(client)("response lost")
    client._session.post.side_effect = error
    with pytest.raises(type(error)):
        resolve(client._get_token())
    client._session.post.assert_called_once()


def test_logout_is_not_replayed(client, transport):
    session = client._session
    session.post.side_effect = network_error(client)("response lost")
    resolve(client.close())
    session.post.assert_called_once()


@pytest.mark.parametrize("status", [400, 401, 403, 404])
def test_terminal_http_errors_are_not_retried(client, transport, status):
    client._session.post.return_value = transport(status)
    with pytest.raises(FMGHTTPException):
        resolve(client.get({"url": "/example"}))
    client._session.post.assert_called_once()


def test_api_validation_errors_are_not_retried(client, transport):
    response = transport(payload={"result": [{"status": {"code": -10}}]})
    client._session.post.return_value = response
    with pytest.raises(FMGInvalidDataException):
        resolve(client.get({"url": "/example"}))
    client._session.post.assert_called_once()


def test_invalid_json_is_not_retried(client, transport):
    response = transport()
    response.json.side_effect = ValueError("not JSON")
    client._session.post.return_value = response
    with pytest.raises(FMGUnhandledException):
        resolve(client.get({"url": "/example"}))
    client._session.post.assert_called_once()
    released(client, response).assert_called_once_with()


def test_native_timeout_is_retried_for_reads(client, transport):
    error_type = asyncio.TimeoutError if isinstance(client, AsyncFMG) else requests.Timeout
    client._session.post.side_effect = [error_type(), transport()]
    assert resolve(client.get({"url": "/example"})).success
    assert client._session.post.call_count == 2  # noqa: PLR2004


def test_backoff_is_shared_and_capped(client, transport, monkeypatch):
    client._settings.retry_attempts = 4
    client._settings.retry_delay = 0.1
    client._settings.retry_max_delay = 0.15
    asynchronous = isinstance(client, AsyncFMG)
    sleep = AsyncMock() if asynchronous else Mock()
    target = "asyncio.sleep" if asynchronous else "time.sleep"
    monkeypatch.setattr(f"pyresilience._executor.{target}", sleep)
    client._session.post.side_effect = [network_error(client)("disconnected")] * 3 + [transport()]
    assert resolve(client.get({"url": "/example"})).success
    assert [call.args[0] for call in sleep.call_args_list] == pytest.approx([0.1, 0.15, 0.15])


def test_retry_can_be_disabled(client, transport):
    client._settings.retry_attempts = 1
    client._session.post.side_effect = network_error(client)("disconnected")
    with pytest.raises(network_error(client)):
        resolve(client.get({"url": "/example"}))
    client._session.post.assert_called_once()


def test_tls_failure_is_not_retried(client, transport):
    if isinstance(client, AsyncFMG):
        error = aiohttp.ClientSSLError(Mock(), OSError("TLS failed"))
    else:
        error = requests.exceptions.SSLError("TLS failed")
    client._session.post.side_effect = error
    with pytest.raises(type(error)):
        resolve(client.get({"url": "/example"}))
    client._session.post.assert_called_once()


def test_timeout_override_is_applied_and_restored(client, transport):
    original = client._settings.timeout
    client._session.post.return_value = transport()
    with client.timeout(7):
        resolve(client.get({"url": "/example"}))
    timeout = client._session.post.call_args.kwargs["timeout"]
    if isinstance(client, AsyncFMG):
        assert timeout.total is None
        assert timeout.connect == timeout.sock_connect == timeout.sock_read == 7  # noqa: PLR2004
    else:
        assert timeout == 7  # noqa: PLR2004
    assert client._settings.timeout == original


def test_overlapping_async_timeouts_are_isolated(client, transport):
    if not isinstance(client, AsyncFMG):
        return
    client._session.post.return_value = transport()
    original = client._settings.timeout

    async def run():
        first_entered, second_entered, first_exited = asyncio.Event(), asyncio.Event(), asyncio.Event()

        async def first():
            with client.timeout(10):
                first_entered.set()
                await second_entered.wait()
                await client.get({"url": "/first"})
            first_exited.set()

        async def second():
            await first_entered.wait()
            with client.timeout(20):
                second_entered.set()
                await first_exited.wait()
                await client.get({"url": "/second"})

        await asyncio.gather(first(), second())
        await client.get({"url": "/default"})

    asyncio.run(run())
    assert [call.kwargs["timeout"].sock_read for call in client._session.post.call_args_list] == [10, 20, original]
    assert client._settings.timeout == original


def test_nested_timeout_restores_outer_override_after_error(client, transport):
    client._session.post.return_value = transport()
    outer_timeout = 10
    with client.timeout(outer_timeout):
        with pytest.raises(RuntimeError), client.timeout(20):
            raise RuntimeError("inner failed")
        resolve(client.get({"url": "/outer"}))
    timeout = client._session.post.call_args.kwargs["timeout"]
    assert (timeout.sock_read if isinstance(client, AsyncFMG) else timeout) == outer_timeout


@pytest.mark.parametrize("invalid", [0, -1, float("nan"), float("inf")])
def test_invalid_timeout_override_does_not_change_settings(client, invalid):
    original = client._settings.timeout
    with pytest.raises(ValueError), client.timeout(invalid):
        pytest.fail("Invalid timeout was accepted")
    assert client._settings.timeout == original


@pytest.mark.parametrize(
    "field, value",
    [
        ("timeout", 0),
        ("retry_attempts", 0),
        ("retry_delay", -1),
        ("retry_backoff", 0),
        ("retry_max_delay", float("inf")),
    ],
)
def test_invalid_policy_settings(field, value):
    with pytest.raises(ValidationError):
        FMGSettings(base_url="https://example.invalid", username="test", password="test", **{field: value})


def test_sync_retry_stays_on_callers_thread(client, transport):
    if isinstance(client, AsyncFMG):
        return
    thread_id = threading.get_ident()

    def send(*args, **kwargs):
        assert threading.get_ident() == thread_id
        return transport()

    client._session.post.side_effect = send
    assert resolve(client.get({"url": "/example"})).success


def test_async_cancellation_releases_response_without_retry(client, transport):
    if not isinstance(client, AsyncFMG):
        return
    response = transport()
    response.json.side_effect = asyncio.CancelledError()
    client._session.post.return_value = response
    with pytest.raises(asyncio.CancelledError):
        resolve(client.get({"url": "/example"}))
    client._session.post.assert_called_once()
    response.release.assert_called_once_with()


def test_sync_client_import_does_not_require_aiohttp():
    code = """
import importlib.abc
import sys

class BlockAiohttp(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "aiohttp" or fullname.startswith("aiohttp."):
            raise ModuleNotFoundError(fullname, name=fullname)

sys.meta_path.insert(0, BlockAiohttp())
from pyfortinet import FMG, FMGBase
FMG(base_url="https://example.invalid", username="test", password="test")
FMGBase(base_url="https://example.invalid", username="test", password="test")
"""
    subprocess.run([sys.executable, "-c", code], check=True, capture_output=True, text=True)
