"""Invalid high-level requests obey the same error policy."""

import pytest

from pyfortinet.exceptions import FMGWrongRequestException

from .conftest import resolve


@pytest.mark.parametrize("method", ["add", "delete", "update", "set", "exec", "get"])
@pytest.mark.parametrize("raise_on_error", [False, True])
def test_invalid_request(client, post, method, raise_on_error):
    """Report invalid types consistently and never send them to the transport."""
    client.raise_on_error = raise_on_error
    if raise_on_error:
        with pytest.raises(FMGWrongRequestException, match="Wrong type of request received"):
            resolve(getattr(client, method)(42))
    else:
        response = resolve(getattr(client, method)(42))
        assert not response.success
        data = response.data if isinstance(response.data, dict) else response.data[0]
        assert "Wrong type of request received" in data["error"]
    post.assert_not_called()
