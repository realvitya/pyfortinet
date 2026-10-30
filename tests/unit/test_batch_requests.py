"""Validate batch writes before contacting the transport."""

from copy import deepcopy

import pytest

from pyfortinet import AsyncFMG, AsyncFMGBase, FMGBase
from pyfortinet.exceptions import FMGWrongRequestException
from pyfortinet.fmg_api.firewall import Address

from .conftest import resolve


@pytest.mark.parametrize("method", ["add", "update", "set", "delete"])
@pytest.mark.parametrize("raise_on_error", [False, True])
@pytest.mark.parametrize("invalid", ["empty", "mixed_objects", "mixed_dicts", "bad_member"])
def test_invalid_high_level_batch(client, post, method, raise_on_error, invalid):
    address = Address(name="example")
    requests = {
        "empty": [],
        "mixed_objects": [address, {"url": "/example"}],
        "mixed_dicts": [{"url": "/example"}, address],
        "bad_member": [address, 42],
    }
    client.raise_on_error = raise_on_error
    if raise_on_error:
        with pytest.raises(FMGWrongRequestException):
            resolve(getattr(client, method)(requests[invalid]))
    else:
        response = resolve(getattr(client, method)(requests[invalid]))
        assert not response.success
        assert response.data[0]["error"]
    assert address.fmg_scope is None
    post.assert_not_called()


@pytest.mark.parametrize("method", ["add", "update", "set", "delete", "clone"])
@pytest.mark.parametrize("raise_on_error", [False, True])
@pytest.mark.parametrize("batch", [[], [{"url": "/example"}, 42]])
def test_invalid_low_level_batch(client, post, method, raise_on_error, batch):
    client.raise_on_error = raise_on_error
    base = AsyncFMGBase if isinstance(client, AsyncFMG) else FMGBase
    if raise_on_error:
        with pytest.raises(FMGWrongRequestException):
            resolve(getattr(base, method)(client, batch))
    else:
        response = resolve(getattr(base, method)(client, batch))
        assert not response.success
    post.assert_not_called()


@pytest.mark.parametrize("method", ["add", "update", "set", "delete"])
@pytest.mark.parametrize("objects", [False, True])
def test_valid_batches_preserve_order(client, post, method, objects):
    requests = (
        [Address(name=name) for name in ["first", "second"]]
        if objects
        else [{"url": f"/example/{name}", "data": {"name": name}} for name in ["first", "second"]]
    )
    original = deepcopy(requests)
    post.return_value = [{"status": {"code": 0}}, {"status": {"code": 0}}]
    assert resolve(getattr(client, method)(requests)).success
    params = post.call_args.kwargs["request"]["params"]
    if objects:
        assert [param["url"].split("/")[-1] for param in params] == (
            ["address", "address"] if method == "add" else ["first", "second"]
        )
    else:
        assert [param["url"] for param in params] == [item["url"] for item in original]
        assert requests == original
