"""Response indexing handles supported object and dictionary shapes."""

import pytest

from pyfortinet import AsyncFMGResponse, FMGResponse
from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.firewall import Address


@pytest.fixture(params=[FMGResponse, AsyncFMGResponse], ids=["sync", "async"])
def response_type(request):
    return request.param


def test_single_dictionary_response_lookup(response_type):
    item = {"data": {"name": "example"}, "status": {"code": 0}}
    response = response_type(data=item, success=True)
    assert response[0] is item
    assert response["example", "name"] is item
    assert response["missing", "name"] is None
    with pytest.raises(IndexError):
        _ = response[1]


def test_lookup_skips_results_without_object_data(response_type):
    response = response_type(data=[{"data": None}, {"error": "failed"}])
    assert response["example", "name"] is None


def test_object_lookup_with_explicit_key(response_type):
    class UnkeyedObject(FMGObject):
        name: str

    obj = UnkeyedObject(name="example")
    response = response_type(data=[obj], success=True)
    assert response["example", "name"] is obj
    with pytest.raises(ValueError, match="Invalid key"):
        _ = response["example"]


def test_object_lookup_retains_default_master_key(response_type):
    obj = Address(name="example")
    response = response_type(data=[obj], success=True)
    assert response["example"] is obj
    assert response["missing"] is None
