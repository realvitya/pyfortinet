"""Task polling parity without sleeping or accessing a device."""

from unittest.mock import AsyncMock, Mock

import aiohttp
import pytest
from requests.exceptions import ConnectionError as RequestsConnectionError

from pyfortinet import AsyncFMG, FMGResponse
from tests.unit.conftest import resolve


@pytest.fixture
def polling(client, monkeypatch):
    """Replace task reads and delays, preserving async semantics."""
    asynchronous = isinstance(client, AsyncFMG)
    mock_type = AsyncMock if asynchronous else Mock
    client.get = mock_type()
    module = "pyfortinet.fmg_api.async_fmgbase" if asynchronous else "pyfortinet.fmg_api.fmgbase"
    monkeypatch.setattr(f"{module}.{'asyncio' if asynchronous else 'time'}.sleep", mock_type())
    done = {"adom": 0, "end_tm": 0, "flags": 0, "id": 12, "line": [], "percent": 100, "state": "done"}
    client.get.return_value = FMGResponse(data=[{"data": [done], "status": {"code": 0}}], success=True)
    return client.get


@pytest.mark.parametrize("key", ["task", "taskid"])
def test_task_identifier_spellings(client, polling, key):
    response = FMGResponse(data=[{"data": {key: 12}}], success=True)
    callback = Mock()
    assert resolve(client.wait_for_task(response, callback=callback)) == "done"
    callback.assert_called_once_with(100, "")
    assert polling.call_args.args[0]["filter"] == ["id", "==", 12]


def test_warning_task_returns_without_polling_again(client, polling):
    polling.return_value.data[0]["data"][0]["state"] = "warning"
    assert resolve(client.wait_for_task(12)) == "warning"
    polling.assert_called_once()


@pytest.mark.parametrize("timeout", [60, -1])
def test_task_connection_retry(client, polling, timeout):
    """Retry transient failures and report the requested ID on timeout."""
    error = aiohttp.ClientConnectionError if isinstance(client, AsyncFMG) else RequestsConnectionError
    polling.side_effect = [error("disconnected"), polling.return_value]
    if timeout < 0:
        with pytest.raises(TimeoutError, match="task 12"):
            resolve(client.wait_for_task(12, timeout=timeout))
    else:
        assert resolve(client.wait_for_task(12)) == "done"
        assert polling.call_count == 2  # noqa: PLR2004


def test_async_callable_callback(client, polling):
    """Await callbacks implemented as callable objects as well as functions."""
    if not isinstance(client, AsyncFMG):
        return

    class Callback:
        def __init__(self):
            self.calls = []

        async def __call__(self, percent, detail):
            self.calls.append((percent, detail))

    callback = Callback()
    assert resolve(client.wait_for_task(12, callback=callback)) == "done"
    assert callback.calls == [(100, "")]


@pytest.mark.parametrize("data", [[], {}, {"data": None}, [{"data": None}], [{"data": []}]])
def test_response_without_task_metadata_is_not_polled(client, polling, data):
    response = FMGResponse(data=data, success=True)
    assert resolve(client.wait_for_task(response)) is None
    polling.assert_not_called()


def test_failed_task_creation_response_is_not_polled(client, polling):
    response = FMGResponse(data=[{"data": {"taskid": 12}}], success=False)
    assert resolve(client.wait_for_task(response)) is None
    polling.assert_not_called()


def test_failed_status_read_does_not_invoke_progress_callback(client, polling):
    polling.return_value = FMGResponse(data=[{"error": "permission denied"}], success=False)
    callback = Mock()
    assert resolve(client.wait_for_task(12, callback=callback)) is None
    polling.assert_called_once()
    callback.assert_not_called()
