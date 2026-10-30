"""JSON-RPC metadata parity between clients."""

from .conftest import resolve


def test_version_request_uses_connection_id(client, post):
    client._id = 73
    post.return_value = {"data": {"Version": "example-version"}}
    assert resolve(client.get_version()) == "example-version"
    request = post.call_args.args[0]
    assert request["id"] == client._id
    assert request["session"] == client._token.get_secret_value()
