"""Fortimanager settings"""

from typing import Annotated

from pydantic import Field, SecretStr, field_validator
from pydantic.networks import HttpUrl
from pydantic_settings import BaseSettings


class FMGSettings(BaseSettings):
    """Fortimanager settings

    Attributes:
        base_url (str): Base URL to access FMG (e.g.: https://myfmg/jsonrpc)
        username (str): User to authenticate
        password (str): Password for authentication
        adom (str): ADOM to use for this connection
        verify (bool): Verify SSL certificate (REQUESTS_CA_BUNDLE can set accepted CA cert)
        timeout (float): Connection timeout for requests in seconds
        raise_on_error (bool): Raise exception on error
    """

    base_url: Annotated[HttpUrl, Field(description="Base URL to access FMG (e.g.: https://myfmg/jsonrpc)")]
    username: Annotated[str, Field(description="User to authenticate")]
    password: Annotated[SecretStr, Field(description="Password for authentication")]
    adom: Annotated[str, Field(description="ADOM to use for this connection")] = "global"
    verify: Annotated[
        bool, Field(description="Verify SSL certificate (REQUESTS_CA_BUNDLE can set accepted CA cert)")
    ] = True
    timeout: Annotated[float, Field(description="Connection timeout for requests in seconds")] = 120.0
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
