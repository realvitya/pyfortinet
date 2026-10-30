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
    response.status_code = response.status = 200
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


def test_repeated_open_keeps_existing_session(client, session):
    resolve(client.open())
    client.lock._uses_workspace = True
    client.lock.locked_adoms.add("other")
    assert resolve(client.open()) is client
    client._get_token.assert_called_once_with()
    assert client._session is session
    assert client.lock.locked_adoms == {"other"}
    assert client.lock.uses_workspace is True
    session.close.assert_not_called()


def test_close_without_open_is_safe(client, session):
    resolve(client.close())
    assert client._session is None
    assert client._token is None
    session.post.assert_not_called()


def test_repeated_close_is_safe(client, session):
    resolve(client.open())
    resolve(client.close())
    resolve(client.close())
    session.close.assert_called_once_with()
    session.post.assert_called_once()
    assert client._session is None
    assert client._token is None


@pytest.mark.parametrize("failure", ["logout", "decode", "session_close", "workspace"])
def test_close_cleans_up_on_errors(client, session, failure):
    resolve(client.open())
    client.lock._uses_workspace = True
    client.lock.locked_adoms.add("other")
    mock_type = AsyncMock if isinstance(client, AsyncFMG) else Mock
    client.lock.commit_changes = mock_type()
    client.lock.unlock_adoms = mock_type()
    targets = {
        "logout": session.post,
        "decode": session.post.return_value.json,
        "session_close": session.close,
        "workspace": client.lock.commit_changes,
    }
    targets[failure].side_effect = RuntimeError("cleanup failed")
    with pytest.raises(RuntimeError, match="cleanup failed"):
        resolve(client.close())
    session.close.assert_called_once_with()
    assert client._session is None
    assert client._token is None
    assert not client.lock.locked_adoms
    assert client.lock.uses_workspace is None


def test_cancelled_logout_cleans_up(client, session):
    if not isinstance(client, AsyncFMG):
        return
    resolve(client.open())
    session.post.side_effect = asyncio.CancelledError()
    with pytest.raises(asyncio.CancelledError):
        resolve(client.close())
    session.close.assert_awaited_once_with()
    assert client._session is None
    assert client._token is None


@pytest.mark.parametrize("configured_discard", [False, True])
@pytest.mark.parametrize("discard_changes", [False, True])
def test_close_discard_policy_is_not_sticky(client, session, configured_discard, discard_changes):
    """A per-close discard request must not change future connection behavior."""
    client.discard_on_close = configured_discard
    mock_type = AsyncMock if isinstance(client, AsyncFMG) else Mock
    client.lock.commit_changes = mock_type()
    client.lock.unlock_adoms = mock_type()
    resolve(client.open())
    client.lock._uses_workspace = True
    resolve(client.close(discard_changes=discard_changes))
    assert client.discard_on_close is configured_discard
    resolve(client.open())
    client.lock._uses_workspace = True
    resolve(client.close())
    expected_commits = int(not configured_discard and not discard_changes) + int(not configured_discard)
    assert client.lock.commit_changes.call_count == expected_commits
