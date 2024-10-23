"""FMG API library"""
import re
from abc import ABC
from typing import Optional, TYPE_CHECKING, TypeVar, Literal, Union

from pydantic import BaseModel

if TYPE_CHECKING:
    from pyfortinet import FMG, AsyncFMG

    AnyFMG = Union[FMG, AsyncFMG]
from pyfortinet.exceptions import FMGMissingScopeException, FMGNotAssignedException, FMGInvalidURL

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

    def __hash__(self):
        return hash(self.model_dump_json(by_alias=True, exclude_none=True, exclude_unset=True, exclude_defaults=True))

    def get_url(self, method: Literal["get", "add", "set", "update", "delete", "clone", "exec"] = "exec") -> str:
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
        _master_keys (str): attributes which represents unique key in FMG DB for this API class
    """

    _master_keys: Optional[dict[str, str]] = None

    @property
    def master_keys(self) -> dict[str, str]:
        """Dict of fields where key is URL attribute and value is model field

        Example of master_keys definition:
        URL: /pm/config/{scope}/obj/firewall/addrgrp/{addrgrp}
        master_keys = {"addrgrp": "name"}

        Here "addrgrp" is the URL field to be replaced by the model field "name"
        """
        return self._master_keys

    def get_url(self, method: Literal["get", "add", "set", "update", "delete", "clone", "exec"] = "get") -> str:
        """General API URL assembly

        To be overridden by more complex API URLs in different classes
        """
        variables = re.findall(r"{(.*?)}", self._url)
        if not self.fmg_scope:
            if "scope" in variables:
                raise FMGMissingScopeException(f"Missing scope for {self}")
        url = self._url
        for field in variables:
            if field == "scope":
                url = url.replace(f"{{{field}}}", self.fmg_scope)
            else:
                if hasattr(self, field) and getattr(self, field) is not None:
                    url = url.replace(f"{{{field}}}", getattr(self, field))
                elif (
                        method in ("get", "set", "update", "delete", "clone")
                        and field in self.master_keys
                        and getattr(self, self.master_keys[field], None) is not None
                ):  # certain methods require master key (like policyid)
                    url = url.replace(f"{{{field}}}", getattr(self, self.master_keys[field]))
                # delete field from URL if no data found (can lead to errors)
                elif method in ("get", "add", "set", "update") and url.endswith(f"{{{field}}}"):
                    url = url.replace(f"/{{{field}}}", "")
                else:
                    raise FMGInvalidURL(f"Missing field '{field}' for ({self._url})")
        return url

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

    def model_dump_for_filter(self) -> dict:
        """Modified pydantic model dump for FMG API

        This method will include otherwise excluded fields to use them in FMG.get method filtering.
        Special attention is made for URL fields which must not be included in the filters as they are not part of the
        payload.
        """
        # get the normal dump first
        dump = self.model_dump(by_alias=True, exclude_none=True)
        # include excluded not-none fields
        excluded_fields = {}
        for field_name, field_model in self.model_fields.items():
            # check only excluded vars which are not None and are not URL attributes (cannot be used as filter)
            if field_model.exclude and getattr(self, field_name) is not None and f"{{{field_name}}}" not in self._url:
                excluded_fields[field_model.serialization_alias or field_name] = getattr(self, field_name)

        dump.update(excluded_fields)
        return dump


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
