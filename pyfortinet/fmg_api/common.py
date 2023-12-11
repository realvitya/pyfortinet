"""Commmon objects"""
from typing import Literal, Optional

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

MGMT_MODE = Literal["unreg", "fmg", "faz", "fmgfaz"]
OS_TYPE = Literal[
    "unknown",
    "fos",
    "fsw",
    "foc",
    "fml",
    "faz",
    "fwb",
    "fch",
    "fct",
    "log",
    "fmg",
    "fsa",
    "fdd",
    "fac",
    "fpx",
    "fna",
    "ffw",
    "fsr",
    "fad",
    "fdc",
    "fap",
    "fxt",
    "fts",
    "fai",
    "fwc",
    "fis",
    "fed",
]
OS_VER = Literal["unknown", "0.0", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0"]


@dataclass
class Scope:
    """Specify scope for an object"""

    name: str
    vdom: str


@dataclass
class Result:
    """API result"""

    code: int
    message: str


class BaseDevice(BaseModel):
    # api attributes
    name: Optional[str] = None
    adm_usr: Optional[str] = None
    adm_pass: Optional[list[str]] = None
    desc: Optional[str] = None
    ip: Optional[str] = None
    meta_fields: Optional[dict[str, str]] = Field(None, serialization_alias="meta fields")
    mgmt_mode: Optional[MGMT_MODE] = None
    os_type: Optional[OS_TYPE] = None
    os_ver: Optional[OS_VER] = None
    patch: Optional[int] = None
    sn: Optional[str] = Field(None, description="Serial number")
