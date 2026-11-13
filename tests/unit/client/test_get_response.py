"""Low-level GET response parity."""

from copy import deepcopy
from unittest.mock import AsyncMock, Mock

import pytest

from pyfortinet import AsyncFMG, AsyncFMGBase, FMGBase
from pyfortinet.exceptions import FMGObjectNotExistException, FMGUnhandledException
from tests.lab.resources import AsyncLabResources, LabResources
from tests.unit.conftest import resolve


@pytest.mark.parametrize("data", [[], {}, None, [{"name": "example"}]])
def test_low_level_get_preserves_successful_result(client, post, data):
    """An empty or absent data value must not turn an OK response into failure."""
    payload = {"data": data, "status": {"code": 0}, "url": "/example"}
    post.return_value = deepcopy(payload)
    response = resolve(client.get({"url": "/example"}))
    assert response.success
    assert response.data == [payload]
    assert response.fmg is client


def test_low_level_get_missing_object(client, post):
    """A missing object is a successful empty lookup with the normal result shape."""
    post.side_effect = FMGObjectNotExistException("missing")
    response = resolve(client.get({"url": "/example"}))
    assert response.success
    assert response.data == [{"data": [], "status": {"code": 0}}]
    assert response.fmg is client


def test_missing_object_can_be_reserved_and_cleaned_up(client, post):
    """The real client response works with the live-test ownership helper."""
    post.side_effect = FMGObjectNotExistException("missing")
    resources = AsyncLabResources(client) if isinstance(client, AsyncFMG) else LabResources(client)
    assert resolve(resources.reserve("/example")) == "/example"
    resolve(resources.cleanup())
    assert all(call.kwargs["request"]["method"] == "get" for call in post.call_args_list)


@pytest.mark.parametrize("payload", [{"result": []}, {"result": [{"data": ""}]}])
def test_transport_empty_response(client, monkeypatch, payload):
    """Malformed result envelopes raise a library exception in both clients."""
    asynchronous = isinstance(client, AsyncFMG)
    response = Mock()
    response.status_code = response.status = 200
    response.json = AsyncMock(return_value=payload) if asynchronous else Mock(return_value=payload)
    client._session = Mock()
    client._session.post = AsyncMock(return_value=response) if asynchronous else Mock(return_value=response)
    base = AsyncFMGBase if asynchronous else FMGBase
    with pytest.raises(FMGUnhandledException, match="Malformed JSON-RPC response"):
        resolve(base._post(client, {"method": "get"}))
