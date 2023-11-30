"""FMG API library"""
from abc import ABC
from typing import Any

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class FMGObject(BaseModel, ABC):
    """Abstract base object for all high-level objects

    Attributes:
        scope (str): FMG selected scope (adom or global)
    """

    _url: str
    scope: str = Field("root", exclude=True)

    @property
    def url(self):
        """API URL where {scope} is replaced on the fly based on the FMG selected scope (adom or global)"""
        return self._url

    @classmethod
    @field_validator("_url")
    def construct_url(cls, v: str, info: ValidationInfo):
        """rewrite URL with actual scope"""
        return v.replace("{scope}", info.data["scope"])


class FMGExecObject(FMGObject, ABC):
    _data: Any

    @property
    def data(self):
        return self._data
