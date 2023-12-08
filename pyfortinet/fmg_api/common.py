"""Commmon objects"""
from pydantic.dataclasses import dataclass


@dataclass
class Scope:
    """Specify scope for an object"""

    name: str
    vdom: str


@dataclass
class Result:
    code: int
    message: str
