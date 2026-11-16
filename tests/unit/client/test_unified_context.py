"""One public FMG entry point supports typed sync and async connection contexts."""

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest

from pyfortinet import FMG, AsyncFMG, FMGBase
from pyfortinet.exceptions import FMGConfigurationException, FMGTokenException
from pyfortinet.fmg_api.firewall import Address


@pytest.fixture
def manager():
    return FMG(base_url="https://example.invalid", username="test", password="test", adom="root")


@pytest.mark.parametrize("asynchronous", [False, True])
def test_context_requests_and_object_methods(manager, monkeypatch, asynchronous):
    mock_type = AsyncMock if asynchronous else Mock

    def response(data=None, **extra):
        result = Mock(status_code=200, status=200)
        result.json = mock_type(return_value={"result": [{"status": {"code": 0}, "data": data}], **extra})
        return result

    session = Mock()
    session.close = mock_type()
    session.post = mock_type(
        side_effect=[response(session="session-token"), response([{"name": "example"}]), response(), response()]
    )
    factory = "aiohttp.ClientSession" if asynchronous else "requests.Session"
    monkeypatch.setattr(factory, Mock(return_value=session))

    async def use_async():
        async with manager as client:
            assert isinstance(client, AsyncFMG)
            address = (await client.get(Address)).first()
            assert address._fmg is client
            address.comment = "updated"
            assert (await address.update()).success

    if asynchronous:
        asyncio.run(use_async())
    else:
        with manager as client:
            assert client is manager
            address = client.get(Address).first()
            assert address._fmg is client
            address.comment = "updated"
            assert address.update().success
    assert [call.kwargs["json"]["method"] for call in session.post.call_args_list] == ["exec", "get", "update", "exec"]
    session.close.assert_called_once_with()
    assert manager._async_context is None
    assert manager._session is None


@pytest.fixture
def async_lifecycle(monkeypatch):
    open_client, close_client = AsyncMock(), AsyncMock()
    monkeypatch.setattr(AsyncFMG, "open", open_client)
    monkeypatch.setattr(AsyncFMG, "close", close_client)
    return open_client, close_client


@pytest.mark.parametrize("fail", [False, True])
def test_async_context_propagates_exceptions_and_discard_policy(manager, async_lifecycle, fail):
    async def run():
        async with manager as client:
            assert isinstance(client, AsyncFMG)
            if fail:
                raise RuntimeError("operation failed")

    if fail:
        with pytest.raises(RuntimeError, match="operation failed"):
            asyncio.run(run())
    else:
        asyncio.run(run())
    async_lifecycle[1].assert_awaited_once_with(discard_changes=fail)
    assert manager._async_context is None


@pytest.mark.parametrize("error", [FMGTokenException("login failed"), asyncio.CancelledError()])
def test_async_entry_failure_allows_reuse(manager, async_lifecycle, error):
    async_lifecycle[0].side_effect = [error, None]

    async def run():
        with pytest.raises(type(error)):
            async with manager:
                pytest.fail("Connection unexpectedly opened")
        async with manager as client:
            assert isinstance(client, AsyncFMG)

    asyncio.run(run())
    async_lifecycle[1].assert_awaited_once()
    assert manager._async_context is None


def test_async_cleanup_failure_allows_reuse(manager, async_lifecycle):
    async_lifecycle[1].side_effect = [RuntimeError("cleanup failed"), None]

    async def run():
        with pytest.raises(RuntimeError, match="cleanup failed"):
            async with manager:
                pass
        async with manager as client:
            assert isinstance(client, AsyncFMG)

    asyncio.run(run())
    assert manager._async_context is None


def test_overlapping_async_contexts_do_not_close_the_outer_client(manager, async_lifecycle):
    async def run():
        async with manager as client:
            with pytest.raises(FMGConfigurationException, match="already has an active"):
                async with manager:
                    pytest.fail("Nested connection unexpectedly opened")
            assert manager._async_context is client
            async_lifecycle[1].assert_not_called()

    asyncio.run(run())
    async_lifecycle[0].assert_awaited_once()
    async_lifecycle[1].assert_awaited_once()


@pytest.mark.parametrize("method", ["open", "close"])
def test_sync_lifecycle_cannot_interrupt_async_context(manager, async_lifecycle, monkeypatch, method):
    sync_method = Mock()
    monkeypatch.setattr(FMGBase, method, sync_method)

    async def run():
        async with manager:
            with pytest.raises(FMGConfigurationException, match="client bound by 'async with'"):
                getattr(manager, method)()

    asyncio.run(run())
    sync_method.assert_not_called()


def test_async_context_cannot_replace_open_sync_session(manager, async_lifecycle):
    manager._session = Mock()
    with pytest.raises(FMGConfigurationException, match="already has an active"):
        asyncio.run(manager.__aenter__())
    async_lifecycle[0].assert_not_called()


def test_configuration_is_shared_between_contexts(manager, async_lifecycle):
    manager.raise_on_error = False

    async def run():
        async with manager as client:
            assert client.adom == manager.adom
            assert client.raise_on_error is False
            client.adom = "other"
            client.raise_on_error = True

    asyncio.run(run())
    assert manager.adom == "other"
    assert manager.raise_on_error is True


def test_manager_can_switch_context_modes_sequentially(manager, async_lifecycle, monkeypatch):
    def open_sync(client):
        client._session = Mock()

    def close_sync(client, discard_changes=False):
        client._session = None

    monkeypatch.setattr(FMGBase, "open", open_sync)
    monkeypatch.setattr(FMGBase, "close", close_sync)

    async def run():
        async with manager as client:
            assert isinstance(client, AsyncFMG)

    with manager as client:
        assert client is manager
    asyncio.run(run())
    with manager as client:
        assert client is manager
    assert manager._session is None
    async_lifecycle[1].assert_awaited_once()
