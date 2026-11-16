"""Fortimanager settings"""

from typing import Annotated

from pydantic import Field, SecretStr, field_validator
from pydantic.networks import HttpUrl
from pydantic_settings import BaseSettings


class FMGSettings(BaseSettings):
    """Connection and resilience settings for FortiManager clients.

    Attributes:
        base_url: FortiManager HTTPS URL; /jsonrpc is appended if absent.
        username: Account with JSON-RPC API access.
        password: Authentication password, stored as a Pydantic SecretStr.
        adom: Selected ADOM or "global" for the Global Database. Defaults to "global".
        verify: Verify TLS certificates. Defaults to True. REQUESTS_CA_BUNDLE applies to the sync transport.
        timeout: Connect/read inactivity timeout per transport attempt, in seconds.
        retry_attempts: Maximum transport attempts for read requests, including the initial call.
        retry_delay: Initial retry delay in seconds.
        retry_backoff: Retry delay multiplier.
        retry_max_delay: Maximum retry delay in seconds.
        retry_jitter: Randomize retry delays.
        raise_on_error: Raise library exceptions for decorated API operations instead of failed responses.
        discard_on_close: Skip workspace commits during close. Defaults to False.
        discard_on_error: Skip workspace commits when an exception exits the context. Defaults to True.

    Notes:
        Discard settings do not reverse configuration installations or every device operation.
    """

    base_url: Annotated[HttpUrl, Field(description="Base URL to access FMG (e.g.: https://myfmg/jsonrpc)")]
    username: Annotated[str, Field(description="User to authenticate")]
    password: Annotated[SecretStr, Field(description="Password for authentication")]
    adom: Annotated[str, Field(description="ADOM to use for this connection")] = "global"
    verify: Annotated[
        bool, Field(description="Verify SSL certificate (REQUESTS_CA_BUNDLE can set accepted CA cert)")
    ] = True
    timeout: Annotated[float, Field(gt=0, allow_inf_nan=False, description="Connect/read timeout in seconds")] = 120.0
    retry_attempts: Annotated[int, Field(ge=1, description="Total transport attempts for read requests")] = 3
    retry_delay: Annotated[float, Field(ge=0, allow_inf_nan=False, description="Initial retry delay in seconds")] = 0.1
    retry_backoff: Annotated[float, Field(ge=1, allow_inf_nan=False, description="Retry delay multiplier")] = 2.0
    retry_max_delay: Annotated[
        float, Field(ge=0, allow_inf_nan=False, description="Maximum retry delay in seconds")
    ] = 2.0
    retry_jitter: bool = True
    raise_on_error: Annotated[bool, Field(description="Raise exception on error")] = True
    discard_on_close: Annotated[bool, Field(description="Discard changes after connection close (workspace mode)")] = (
        False
    )
    discard_on_error: Annotated[bool, Field(description="Discard changes when exception occurs (workspace mode)")] = (
        True
    )

    @field_validator("base_url", mode="before")
    def check_base_url(cls, v: str):
        """check and fix base_url"""
        v = v.rstrip("/ ")
        if not v.endswith("/jsonrpc"):
            v += "/jsonrpc"
        return HttpUrl(v)
