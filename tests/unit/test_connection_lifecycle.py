"""Connection cleanup without live HTTP sessions."""

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest
from pydantic import SecretStr

from pyfortinet import AsyncFMG
from pyfortinet.exceptions import FMGTokenException

from .conftest import resolve


@pytest.fixture
def session(client, monkeypatch):
    """Replace HTTP session creation and logout, retaining await conventions."""
    asynchronous = isinstance(client, AsyncFMG)
    mock_type = AsyncMock if asynchronous else Mock
    session = Mock()
    session.close = mock_type()
    response = Mock()
    response.json = mock_type(return_value={"result": [{"status": {"code": 0}}]})
    session.post = mock_type(return_value=response)
    factory = "aiohttp.ClientSession" if asynchronous else "requests.Session"
    monkeypatch.setattr(factory, Mock(return_value=session))
    monkeypatch.setattr(client, "_get_token", mock_type(return_value=SecretStr("session")))
    client._token = None
    return session


@pytest.mark.parametrize("error", [FMGTokenException, RuntimeError])
def test_failed_login_closes_session(client, session, error):
    client._get_token.side_effect = error("login failed")
    with pytest.raises(error, match="login failed"):
        resolve(client.open())
    session.close.assert_called_once_with()
    assert client._session is None
    assert client._token is None


def test_cancelled_login_closes_session(client, session):
    if not isinstance(client, AsyncFMG):
        return
    client._get_token.side_effect = asyncio.CancelledError()
    with pytest.raises(asyncio.CancelledError):
        resolve(client.open())
    session.close.assert_awaited_once_with()
    assert client._session is None
    assert client._token is None


def test_open_returns_authenticated_client(client, session):
    assert resolve(client.open()) is client
    assert client._session is session
    assert client._token.get_secret_value() == "session"
    session.close.assert_not_called()
