"""Login response validation shared by both transports."""

from unittest.mock import AsyncMock, Mock

import pytest

from pyfortinet import AsyncFMG
from pyfortinet.exceptions import FMGTokenException, FMGUnhandledException

from .conftest import resolve


@pytest.fixture
def login_response(client):
    asynchronous = isinstance(client, AsyncFMG)
    response = Mock()
    response.status_code = response.status = 200
    response.json = AsyncMock() if asynchronous else Mock()
    client._session = Mock()
    client._session.post = AsyncMock(return_value=response) if asynchronous else Mock(return_value=response)
    return response


@pytest.mark.parametrize(
    "payload",
    [
        None,
        {},
        {"result": []},
        {"result": None},
        {"result": [None]},
        {"result": [{"status": None}]},
        {"result": [{"status": {"code": 0}}]},
        {"result": [{"status": {"code": 0}}], "session": ""},
        {"result": [{"status": {"code": 0}}], "session": 42},
    ],
)
def test_malformed_login_is_rejected(client, login_response, payload):
    login_response.json.return_value = payload
    with pytest.raises(FMGTokenException):
        resolve(client._get_token())


@pytest.mark.parametrize("message", [None, "Wrong credentials"])
def test_login_failure_without_message(client, login_response, message):
    login_response.json.return_value = {"result": [{"status": {"code": -1, "message": message}}]}
    with pytest.raises(FMGTokenException, match="wrong credentials"):
        resolve(client._get_token())


def test_login_permission_error(client, login_response):
    login_response.json.return_value = {"result": [{"status": {"code": -1, "message": "No permission for resource"}}]}
    with pytest.raises(FMGUnhandledException, match="No permission for resource"):
        resolve(client._get_token())


def test_successful_login_decodes_once(client, login_response):
    login_response.json.return_value = {"result": [{"status": {"code": 0}}], "session": "session-token"}
    token = resolve(client._get_token())
    assert token.get_secret_value() == "session-token"
    login_response.json.assert_called_once_with()
