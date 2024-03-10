"""FMG API library"""
from abc import ABC
from typing import Optional, TYPE_CHECKING, TypeVar

from pydantic import BaseModel

if TYPE_CHECKING:
    from pyfortinet import FMG
from pyfortinet.exceptions import FMGMissingScopeException, FMGNotAssignedException


class FMGObject(BaseModel, ABC):
    """Abstract base object for all high-level objects

    Scope must be set before referencing the url! It's done by FMGBase requests as it defaults all objects to its
    selected ADOM.

    Attributes:
        scope (str): FMG selected scope (adom or global)
        _version (str): Supported API version
        _url (str): template for API URL
        _fmg (FMG): FMG instance
    """

    _version = "7.2.4"
    _url: str
    _scope: str = None
    _fmg: "FMG" = None

    def __init__(self, *args, **kwargs) -> None:
        """Initialize FMGObject

        Keyword Args:
            scope: FMG selected scope (adom)
            fmg (FMG): FMG instance
        """
        super().__init__(*args, **kwargs)
        self.scope = kwargs.get("scope")
        self._fmg: "FMG" = kwargs.get("fmg")

    @property
    def get_url(self) -> str:
        """General API URL assembly

        To be overridden by more complex API URLs in different classes
        """
        if not self.scope:
            if "{scope}" in self._url:
                raise FMGMissingScopeException(f"Missing scope for {self}")
            return self._url
        url = self._url.replace("{scope}", self.scope)
        return url

    @property
    def scope(self) -> str:
        """Object scope (adom)"""
        return self._scope

    @scope.setter
    def scope(self, value: Optional[str] = None):
        if value:
            # if input already in /adom/... then fix it
            self._scope = "global" if value == "global" else f"adom/{value}".replace("adom/adom", "adom")

    def add(self):
        """Add this object to FMG"""
        if self._fmg:
            return self._fmg.add(self)
        raise FMGNotAssignedException

    def set(self):
        """Set FMG operation on this object"""
        if self._fmg:
            return self._fmg.set(self)
        raise FMGNotAssignedException

    def update(self):
        """Update FMG operation on this object"""
        if self._fmg:
            return self._fmg.update(self)
        raise FMGNotAssignedException

    def delete(self):
        """Delete FMG operation on this object"""
        if self._fmg:
            return self._fmg.delete(self)
        raise FMGNotAssignedException


SomeFMGObject = TypeVar("SomeFMGObject", bound=FMGObject)


class FMGExecObject(FMGObject, ABC):
    """FMG execute job type"""

    @property
    def data(self):
        return self.model_dump(by_alias=True)

    def exec(self):
        """Exec FMG operation on this object"""
        if self._fmg:
            return self._fmg.exec(self)
        raise FMGNotAssignedException
