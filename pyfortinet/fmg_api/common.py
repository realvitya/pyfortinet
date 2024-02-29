"""Common objects"""
import re
from typing import Literal, Optional, List, Union

from pydantic import BaseModel, Field, field_validator, IPvAnyAddress
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
DEVICE_ACTION = Literal["add_model", "promote_unreg"]


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
    name: Optional[str] = Field(None, pattern=r"[\w-]{1,36}")
    adm_usr: Optional[str] = Field(None, max_length=36)
    adm_pass: Union[None, str, list[str]] = Field(None, max_length=128)
    desc: Optional[str] = None
    ip: Optional[str] = None
    meta_fields: Optional[dict[str, str]] = Field(None, serialization_alias="meta fields")
    mgmt_mode: Optional[MGMT_MODE] = None
    os_type: Optional[OS_TYPE] = None
    os_ver: Optional[OS_VER] = Field(None, description="Major release no")
    mr: Optional[int] = Field(None, description="Minor release no")
    patch: Optional[int] = Field(None, description="Patch release no")
    sn: Optional[str] = Field(None, description="Serial number")
    device_action: Optional[DEVICE_ACTION] = Field(None, serialization_alias="device action")
    device_blueprint: Optional[str] = Field(None, serialization_alias="device blueprint")

    @field_validator("ip")
    def validate_ip(cls, v):
        """validate input but still represent the string"""
        IPvAnyAddress(v)
        return v

    @field_validator("mgmt_mode", mode="before")
    def validate_mgmt_mode(cls, v):
        """ensure using text variant"""
        if isinstance(v, str):
            return v
        return MGMT_MODE.__dict__.get("__args__")[v]

    @field_validator("os_type", mode="before")
    def validate_os_type(cls, v):
        """ensure using text variant"""
        if isinstance(v, str):
            return v
        return OS_TYPE.__dict__.get("__args__")[v]

    @field_validator("os_ver", mode="before")
    def validate_os_ver(cls, v):
        """ensure using text variant"""
        if isinstance(v, str):
            return v
        elif isinstance(v, int):
            return OS_VER.__dict__.get("__args__")[v]
        raise ValueError(f"Wrong OS version type: {type(v)}")


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
    "not_glob": "!glob",
}


class F:
    """Filter class that allows us to define a single filter for an object

    Argument format is {field}={value} or {field}__{operator}={value}
    Only one argument can be passed!

    Returns:
        Filter object can be used at ``FMG.get`` method
    """

    negate: bool = False
    source: str = ""
    op: str = ""
    targets: Union[List[Union[int, str]], Union[int, str]]

    def __init__(self, **kwargs):
        """Filter initialization"""
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

    def generate(self) -> List[str]:
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

    def __or__(self, other) -> "ComplexFilter":
        return ComplexFilter(self, "||", other)

    def __invert__(self):
        self.negate = not self.negate
        return self

    def __add__(self, other: Union["F", "FilterList"]):
        return FilterList(self, other)


class FilterList:
    """List of F objects"""

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

    def __len__(self):
        return len(self.members)

    def generate(self) -> List[List[str]]:
        """Generate API filter output"""
        return [member.generate() for member in self.members]


class ComplexFilter:
    """Complex handling of filters and their operator"""

    def __init__(
        self,
        a: Union["ComplexFilter", FilterList, F],
        op: Literal["||", "&&"],
        b: Union["ComplexFilter", FilterList, F],
    ):
        self.a = a
        self.op = op
        self.b = b

    def generate(self) -> list:
        """Generate API filter output"""
        out = [self.a.generate(), self.op, self.b.generate()]
        return out

    def __and__(self, other) -> "ComplexFilter":
        return ComplexFilter(self, "&&", other)

    def __or__(self, other):
        return ComplexFilter(self, "||", other)


FILTER_TYPE = Union[F, FilterList, ComplexFilter]


def text_to_filter(text: str) -> FILTER_TYPE:
    """Text to filter object

    Format of the text follows the ``OP`` definition!
    This is a simple text to filter object converter. It does not support more complex logic.
    Simple field comparisons with `and/or and ,` operators are supported. `,` means a simple `or` between same
    type fields.

    structure::

        fname fop fvalue OP fname fop fvalue OP ...
        ----------------    ----------------
            F token              F token

    Examples:
        simple F filter

        >>> text_to_filter('name like host_%').generate()
        ['name', 'like', 'host_%']

        inversing

        >>> text_to_filter('~name like host_%').generate()
        ['!', 'name', 'like', 'host_%']

        simple or function

        >>> text_to_filter('name eq host_1, name eq host_2').generate()
        [['name', '==', 'host_1'], ['name', '==', 'host_2']]

        more complex filter

        >>> text_to_filter('name eq host_1 and conf_status eq insync').generate()
        [['name', '==', 'host_1'], '&&', ['conf_status', '==', 'insync']]

    Args:
        text (str): Text to parse

    Returns:
        FILTER_TYPE: Filter object which can be used in FMG.get calls

     Raises:
         ValueError: text cannot be parsed
     """
    text = text.strip()
    while text:
        # search F tokens
        f_match = re.match(
            rf'(?P<negate>~)?\s*(?P<fname>\w+)\s+(?P<fop>{"|".join(OP.keys())})\s+(?P<fvalue>\S+)(?<![,|&])', text
        )
        if f_match:
            kwargs = {f"{f_match.group('fname')}__{f_match.group('fop')}": f_match.group("fvalue")}
            if f_match.group("negate"):
                f_token = ~F(**kwargs)
            else:
                f_token = F(**kwargs)
        else:
            raise ValueError(f"Couldn't parse '{text}'!")
        text = text[f_match.end():].strip()
        if not text:
            return f_token
        # search list or complex filter ops
        op_match = re.match(rf"(?P<op>and|or|,)\s+", text)
        if op_match:
            op = {"and": "&&", "or": "||", ",": ","}.get(op_match.group("op"))
        else:
            raise ValueError(f"Couldn't parse '{text}'!")
        text = text[op_match.end():].strip()
        f_token2 = text_to_filter(text)
        if op == ",":
            return FilterList(f_token, f_token2)
        else:
            # noinspection PyTypeChecker, PydanticTypeChecker
            return ComplexFilter(f_token, op, f_token2)
