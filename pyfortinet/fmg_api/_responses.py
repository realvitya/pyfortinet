"""Shared interpretation of FortiManager responses."""

from pydantic import SecretStr

from pyfortinet.exceptions import FMGTokenException, FMGUnhandledException


def login_token(payload):
    """Require a successful login result and a nonempty session token."""
    results = payload.get("result") if isinstance(payload, dict) else None
    if not isinstance(results, list) or not results or not isinstance(results[0], dict):
        raise FMGTokenException("Login failed, malformed authentication response")
    status = results[0].get("status")
    if not isinstance(status, dict) or "code" not in status:
        raise FMGTokenException("Login failed, malformed authentication response")
    if status["code"] != 0:
        message = status.get("message")
        if isinstance(message, str) and "No permission for resource" in message:
            raise FMGUnhandledException("No permission for resource, probably user does not have API access!")
        raise FMGTokenException("Login failed, wrong credentials!")
    token = payload.get("session")
    if not isinstance(token, str) or not token:
        raise FMGTokenException("Login failed, missing or invalid session token")
    return SecretStr(token)
