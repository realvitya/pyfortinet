"""FMG API library"""
from abc import ABC
from typing import Any

from pydantic import BaseModel, Field


class FMGObject(BaseModel, ABC):
    """Abstract base object for all high-level objects

    Attributes:
        scope (str): FMG selected scope (adom or global)
        _version (str): Supported API version
        _url (str): template for API URL
    """

    _version = "7.2.4"
    _url: str
    scope: str = Field("root", exclude=True)

    @property
    def url(self) -> str:
        """General API URL assembly

        To be overridden by more complex API URLs in different classes
        """
        scope = "global" if self.scope == "global" else f"adom/{self.scope}"
        url = self._url.replace("{scope}", scope)
        return url


class FMGExecObject(FMGObject, ABC):
    _data: Any

    @property
    def data(self):
        return self._data
