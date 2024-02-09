"""FMG API library"""
from abc import ABC

from pydantic import BaseModel, Field

from pyfortinet.exceptions import FMGMissingScopeException


class FMGObject(BaseModel, ABC):
    """Abstract base object for all high-level objects

    Scope must be set before referencing the url! It's done by FMGBase requests as it defaults all objects to its
    selected ADOM.

    Attributes:
        scope (str): FMG selected scope (adom or global)
        _version (str): Supported API version
        _url (str): template for API URL
    """

    _version = "7.2.4"
    _url: str
    scope: str = Field(None, exclude=True)

    @property
    def url(self) -> str:
        """General API URL assembly

        To be overridden by more complex API URLs in different classes
        """
        if not self.scope and "scope" in self._url:
            raise FMGMissingScopeException(f"Missing scope for {self}")
        scope = "global" if self.scope == "global" else f"adom/{self.scope}"
        url = self._url.replace("{scope}", scope)
        return url


class FMGExecObject(FMGObject, ABC):
    """FMG execute job type"""

    @property
    def data(self):
        return self.model_dump(by_alias=True)
