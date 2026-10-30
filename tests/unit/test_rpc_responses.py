"""Transport response validation follows the public exception policy."""

from unittest.mock import AsyncMock, Mock

import pytest

from pyfortinet import AsyncFMG
from pyfortinet.exceptions import FMGInvalidDataException, FMGUnhandledException

from .conftest import resolve


@pytest.fixture
def http_response(client):
    mock_type = AsyncMock if isinstance(client, AsyncFMG) else Mock
    response = Mock()
    response.status_code = response.status = 200
    response.json = mock_type()
    client._session = Mock()
    client._session.post = mock_type(return_value=response)
    return response


@pytest.mark.parametrize(
    "payload",
    [
        None,
        {},
        {"error": {"code": -1}},
        {"result": []},
        {"result": None},
        {"result": [None]},
        {"result": [{"data": ""}]},
        {"result": [{"status": {}}]},
        {"result": [{"status": {"code": "0"}}]},
    ],
)
@pytest.mark.parametrize("raise_on_error", [False, True])
@pytest.mark.parametrize("method", ["get", "add", "exec"])
def test_malformed_rpc_replies(client, http_response, payload, raise_on_error, method):
    client.raise_on_error = raise_on_error
    http_response.json.return_value = payload
    if raise_on_error:
        with pytest.raises(FMGUnhandledException, match="Malformed JSON-RPC response"):
            resolve(getattr(client, method)({"url": "/example"}))
    else:
        response = resolve(getattr(client, method)({"url": "/example"}))
        assert not response.success
        assert "Malformed JSON-RPC response" in response.data[0]["error"]


def test_invalid_json_becomes_library_error(client, http_response):
    http_response.json.side_effect = ValueError("not JSON")
    with pytest.raises(FMGUnhandledException, match="expected JSON"):
        resolve(client.get({"url": "/example"}))


@pytest.mark.parametrize("multiple", [False, True])
def test_valid_results_are_preserved(client, http_response, multiple):
    results = [{"status": {"code": 0}, "data": {"name": "first"}}]
    if multiple:
        results.append({"status": {"code": 0}, "data": {"name": "second"}})
    http_response.json.return_value = {"result": results}
    assert resolve(client.get({"url": "/example"})).data == results


def test_known_error_mapping_is_preserved(client, http_response):
    http_response.json.return_value = {"result": [{"status": {"code": -10, "message": "invalid"}}]}
    with pytest.raises(FMGInvalidDataException):
        resolve(client.get({"url": "/example"}))
