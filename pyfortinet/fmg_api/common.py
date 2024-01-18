"""Commmon objects"""
from typing import Literal, Optional, List, Union

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
    name: Optional[str] = Field(None, pattern=r"[\w-]{1,48}")
    adm_usr: Optional[str] = None
    adm_pass: Optional[list[str]] = None
    desc: Optional[str] = None
    ip: Optional[str] = None
    meta_fields: Optional[dict[str, str]] = Field(None, serialization_alias="meta fields")
    mgmt_mode: Optional[MGMT_MODE] = None
    os_type: Optional[OS_TYPE] = None
    os_ver: Optional[OS_VER] = Field(None, description="Major release no")
    mr: Optional[int] = Field(None, description="Minor release no")
    patch: Optional[int] = Field(None, description="Patch release no")
    sn: Optional[str] = Field(None, description="Serial number")


"""
Operator	# of target(s)	Descriptions
"=="        1               Equal to
"!="        1               Not equal to
"<"         1               Less than
"<="        1               Less than or equal to
">"         1               Greater than
">="        1               Greater than or equal to
"&"	        1               Bitwise AND, target can be integer value only, test if (source & target) = 0
"&"	        2               Bitwise AND, target can be integer value only, test if (source & target1) = target2
"in"        1 or more       Test if source is one of the values in target
"contain"   1               If source have a list of values, test if it contains target
"like"      1               SQL pattern matching, where target is a string using % (any character) and _ (single 
                            character) wildcard
"!like"     1               Not like, inverse of "like" operation
"glob"      1               Case-sensitive pattern matching with target string using UNIX wildcards
"!glob"     1               Not glob, inverse of "glob" operation
"&&"        1               Logical AND operator for nested filter with multiple criteria, where source and target must
                            be another filter
"||"        1               Logical OR operator for nested filter with multiple criteria, where source and target must
                            be another filter
"""

OP = {
    "eq": "==",
    "neq": "!=",
    "lt": "<",
    "le": "<=",
    "gt": ">",
    "ge": ">=",
    "or": "&",
    "in": "in",
    "contain": "contain",
    "like": "like",
    "not_like": "!like",
    "glob": "glob",
    "not_glob": "!glob"
}


class F:
    negate: bool = False
    source: str = ""
    op: str = ""
    targets: Union[List[Union[int, str]], Union[int, str]]

    def __init__(self, **kwargs):
        """Filter initialization

        We expect calls from

        """
        if len(kwargs) > 1:
            raise ValueError(f"F only accepts one filter condition at a time!")
        for key, value in kwargs.items():
            if "__" in key:
                self.source, self.op = key.split("__")
                if self.op not in OP:
                    raise ValueError(f"Unknown operation: '{self.op}' !")
                self.op = OP[self.op]
            else:
                self.source = key
                self.op = "=="
            self.targets = value

    def generate(self):
        """Generate API filter list"""
        out = []
        if self.negate:
            out.append("!")
        out.append(self.source)
        out.append(self.op)
        if isinstance(self.targets, list):
            out.extend(self.targets)
        else:
            out.append(self.targets)
        return out

    def __and__(self, other) -> "ComplexFilter":
        return ComplexFilter(self, "&&", other)
        # if isinstance(other, type(self)):
        #     return [self.generate(), "&&", other.generate()]
        # elif isinstance(other, list):
        #     return [self.generate(), "&&", other]

    def __or__(self, other) -> "ComplexFilter":
        return ComplexFilter(self, "||", other)
        # if isinstance(other, type(self)):
        #     return [self.generate(), "||", other.generate()]
        # elif isinstance(other, list):
        #     return [self.generate(), "||", other]

    def __invert__(self):
        self.negate = True
        return self

    def __add__(self, other: Union["F", "FilterList"]):
        return FilterList(self, other)


class FilterList:
    members: list[F]

    def __init__(self, *members: Union[F, "FilterList"]):
        self.members = []
        for member in members:
            self + member

    def __add__(self, other: Union[F, "FilterList"]):
        if isinstance(other, F):
            self.members.append(other)
        elif isinstance(other, FilterList):
            self.members.extend(other.members)
        else:
            raise ValueError(f"Elements '{other}' can't be added to FilterList")
        return self

    def __and__(self, other) -> "ComplexFilter":
        return ComplexFilter(self, "&&", other)

    def __or__(self, other) -> "ComplexFilter":
        return ComplexFilter(self, "||", other)

    def generate(self):
        return [member.generate() for member in self.members]


class ComplexFilter:
    def __init__(self,
                 a: Union["ComplexFilter", FilterList, F],
                 op: Literal["||", "&&"],
                 b: Union["ComplexFilter", FilterList, F]):
        self.a = a
        self.op = op
        self.b = b

    def generate(self):
        out = [
            self.a.generate(),
            self.op,
            self.b.generate()
        ]
        return out

    def __and__(self, other) -> "ComplexFilter":
        return ComplexFilter(self, "&&", other)

    def __or__(self, other):
        return ComplexFilter(self, "||", other)
