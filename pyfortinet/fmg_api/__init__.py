"""FMG API library"""

from abc import ABC
from typing import Optional, TYPE_CHECKING, TypeVar, Literal, Union, List

from pydantic import BaseModel

if TYPE_CHECKING:
    from pyfortinet import FMG, AsyncFMG

    AnyFMG = Union[FMG, AsyncFMG]
from pyfortinet.exceptions import FMGMissingScopeException, FMGNotAssignedException, FMGMissingMasterKeyException

GetOption = Literal[
    "extra info",  # returns more info (e.g. timestamps of changes)
    "assignment info",  # returns where this object is assigned to
    "loadsub",  # When enabled, this option is used to instruct the FortiManager to return sub table information.
    "no loadsub",
    "count",  # This option is used to return the number of entries in a given table.
    "syntax",  # It is used to return the schema of a table or object.
    "devinfo",  # This option could be used to obtain a kind of ADOM checksum used to detect whether a change was made.
    "obj flags",
    "datasrc",  # This option is generally used to get list of possible object types and the objects themselves that
    # could be used within an object you want to create or update.
    "chksum",  # This option is used to retrieve the version or checksum of a specific table.
]


class FMGBaseObject(BaseModel, ABC):
    """Abstract base object for all high-level objects

    Scope must be set before referencing the url! It's done by FMGBase requests as it defaults all objects to its
    selected ADOM.

    In case of AsyncFMG, caller must ensure await-ing the request.

    Attributes:
        fmg_scope (str): FMG selected scope (adom or global)
        _version (str): Supported API version
        _url (str): template for API URL
        _fmg (FMG): FMG instance
    """

    _version = "7.2.4"
    _url: str
    _scope: str = None
    _fmg: "AnyFMG" = None

    def __init__(self, *args, **kwargs) -> None:
        """Initialize FMGObject

        Keyword Args:
            scope (str): FMG selected scope (adom or global)
            fmg (AnyFMG): FMG instance
        """
        super().__init__(*args, **kwargs)
        self.fmg_scope = kwargs.get("fmg_scope")
        self._fmg: "AnyFMG" = kwargs.get("fmg")

    @property
    def get_url(self) -> str:
        """General API URL assembly

        To be overridden by more complex API URLs in different classes
        """
        if not self.fmg_scope:
            if "{scope}" in self._url:
                raise FMGMissingScopeException(f"Missing scope for {self}")
            return self._url
        url = self._url.replace("{scope}", self.fmg_scope)
        return url

    @property
    def fmg_scope(self) -> str:
        """Object scope (adom)"""
        return self._scope

    @fmg_scope.setter
    def fmg_scope(self, value: Optional[str] = None):
        if value:
            # if input already in /adom/... then fix it
            self._scope = "global" if value == "global" else f"adom/{value}".replace("adom/adom", "adom")


class FMGObject(FMGBaseObject, ABC):
    """Abstract base object for all high-level objects

    Scope must be set before referencing the url! It's done by FMGBase requests as it defaults all objects to its
    selected ADOM.

    In case of AsyncFMG, caller must ensure await-ing the request.

    Attributes:
        fmg_scope (str): FMG selected scope (adom or global)
        _version (str): Supported API version
        _url (str): template for API URL
        _fmg (FMG): FMG instance
        _master_keys (str): name of attributes which represents unique key in FMG DB for this API class
    """
    _master_keys: Optional[List[str]] = None

    @property
    def master_keys(self) -> List[str]:
        return self._master_keys

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

    def clone(self, create_task: bool = False, **new: str):
        """Clone this object to a new one"""
        if self._fmg:
            return self._fmg.clone(self, create_task=create_task, **new)
        raise FMGNotAssignedException

    def refresh(self):
        """Re-load data from FMG"""
        if self._fmg:
            return self._fmg.refresh(self)
        raise FMGNotAssignedException


class FMGExecObject(FMGBaseObject, ABC):
    """FMG execute job type

    Attributes:
        fmg_scope (str): FMG selected scope (adom or global)
        _version (str): Supported API version
        _url (str): template for API URL
        _fmg (FMG): FMG instance
    """

    @property
    def data(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def exec(self):
        """Exec FMG operation on this object"""
        if self._fmg:
            return self._fmg.exec(self)
        raise FMGNotAssignedException


# Used by typehints to indicate child of FMGObject
AnyFMGObject = TypeVar("AnyFMGObject", FMGObject, FMGExecObject)
