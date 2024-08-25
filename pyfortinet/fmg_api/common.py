"""Common objects"""

import re
from copy import deepcopy
from typing import Literal, List, Union, Optional

from pydantic.dataclasses import dataclass


@dataclass
class Scope:
    """Specify scope for an object

    Attributes:
        name (str): Scope name (e.g. firewall name or group name)
        vdom (str): VDOM if applicable
    """

    name: str
    vdom: Optional[str] = None


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
    Special argument `_sep` can be passed to indicate the search field separator character, if it's not the `_`.
    Only one argument can be passed!

    Filter object can be used at ``FMG.get`` method

    Attributes:
        negate (bool): If true the filter is negated
        source (str): The source is the API attribute we are looking at
        op (str): The operator for the search
        targets (str): The target is the value we are searching for
    """

    negate: bool = False
    source: str = ""
    op: str = ""
    targets: Union[List[Union[int, str]], Union[int, str]]

    def __init__(self, *, _sep="_", **kwargs):
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
            self.source = re.sub(r"(?!^)_", _sep, self.source)
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

    def __and__(self, other):
        if not self.op:
            return other
        if isinstance(other, F):
            return FilterList(self, other, op="&&")
        if isinstance(other, FilterList):
            if other.op == "&&":
                out = deepcopy(other)
                out.members.insert(0, self)
                return out
        return ComplexFilter(self, "&&", other)

    def __or__(self, other):
        if not self.op:
            return other
        if isinstance(other, F):
            return FilterList(self, other, op="||")
        if isinstance(other, FilterList):
            if other.op == "||":
                out = deepcopy(other)
                out.members.insert(0, self)
                return out
        return ComplexFilter(self, "||", other)

    def __invert__(self):
        out = deepcopy(self)
        out.negate = not self.negate
        return out

    def __add__(self, other: Union["F", "FilterList", "ComplexFilter"]):
        if not self.op:
            return other
        if isinstance(other, ComplexFilter):
            return ComplexFilter(self, ",", other)
        return FilterList(self, other, op=",")


class FilterList:
    """List of F objects"""

    members: list[F]
    op: Literal[",", "||", "&&"]

    def __init__(self, *members: Union[F, "FilterList"], op: Literal[",", "||", "&&"]):
        self.members = list(members)
        self.op = op

        # for member in members:
        #     if self.op == ",":
        #         self + member
        #     elif self.op == "||":
        #         self.members.append(member)

    def __add__(self, other: Union[F, "FilterList"]):
        if self.op == ",":
            if isinstance(other, F):
                out = deepcopy(self)
                out.members.append(other)
                return out
            if isinstance(other, FilterList):
                out = deepcopy(self)
                out.members.extend(other.members)
                return out
        return ComplexFilter(self, ",", other)

    def __and__(self, other):
        if self.op == "&&":
            out = deepcopy(self)
            if isinstance(other, F):
                out.members.append(other)
            elif isinstance(other, FilterList):
                out.members.extend(other.members)
            return out
        return ComplexFilter(self, "&&", other)

    def __or__(self, other):
        if self.op == "||":
            out = deepcopy(self)
            if isinstance(other, F):
                out.members.append(other)
            elif isinstance(other, FilterList):
                out.members.extend(other.members)
            return out
        return ComplexFilter(self, "||", other)

    def __len__(self):
        return len(self.members)

    def generate(self) -> List[List[str]]:
        """Generate API filter output"""
        if self.op == ",":
            return [member.generate() for member in self.members]
        else:
            output = []
            for member in self.members:
                output.append(member.generate())
                output.append(str(self.op))
            del output[-1]
            return output


class ComplexFilter:
    """Complex handling of filters and their operator"""

    def __init__(
        self,
        a: Union["ComplexFilter", FilterList, F],
        op: Literal[",", "||", "&&"],
        b: Union["ComplexFilter", FilterList, F],
    ):
        self.a = a
        self.op = op
        self.b = b

    def generate(self) -> list:
        """Generate API filter output"""
        if self.op == ",":
            out = [self.a.generate(), self.b.generate()]
        else:
            out = [self.a.generate(), self.op, self.b.generate()]
        return out

    def __and__(self, other) -> "ComplexFilter":
        return ComplexFilter(self, "&&", other)

    def __or__(self, other):
        return ComplexFilter(self, "||", other)


def find_matching_parenthesis(input_string):
    """Helper function to find matching parenthesis

    Find the index of the closing parenthesis that matches the first opening parenthesis in the input string.

    Args:
        input_string (str): The string to be scanned for matching parentheses.

    Returns:
        (int): The index of the matching closing parenthesis if found, else returns None.
    """
    count = 1
    pos = 1
    while count > 0:
        open_paren_pos = input_string.find("(", pos)
        close_paren_pos = input_string.find(")", pos)
        if (open_paren_pos != -1 and open_paren_pos < close_paren_pos) or close_paren_pos == -1:
            pos = open_paren_pos
            count += 1
        else:
            pos = close_paren_pos
            count -= 1
        if pos == -1:
            return None
        pos += 1

    return pos - 1


FILTER_TYPE = Union[F, FilterList, ComplexFilter]


def text_to_filter(text: str) -> FILTER_TYPE:
    """Text to filter object

    Format of the text follows the ``OP`` definition!
    This is a simple text to filter object converter. Parenthesis are supported.
    Simple field comparisons with `and/or and ,` operators are supported. `,` means a simple `or` between same
    type fields.
    Field name can contain `-` and ` ` characters, refer to API docs for available field names.

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

        >>> assert text_to_filter("(name eq host_1 and (conf_status eq insync or conf_status eq modified))").generate()
        [
            ["name", "==", "host_1"],
            "&&",
            [["conf_status", "==", "insync"], "||", ["conf_status", "==", "modified"]],
        ]

    Args:
        text (str): Text to parse

    Returns:
        FILTER_TYPE: Filter object which can be used in FMG.get calls

     Raises:
         ValueError: text cannot be parsed
    """
    text = text.strip()
    if text.startswith("("):  # search the end of the ()
        end = find_matching_parenthesis(text)
        if end is None:
            raise ValueError(f"Couldn't parse '{text}'!")
        a = text_to_filter(text[1:end])
        remaining = text[end + 1 :]
        if remaining:  # operand should follow
            op = {"and": "&&", "or": "||", ",": ","}.get(remaining.split()[0])
            if op is None:
                raise ValueError(f"Couldn't parse '{text}'!")
            b = text_to_filter(" ".join(remaining.split()[1:]))
            # noinspection PyTypeChecker
            return ComplexFilter(a, op, b)  # treat parentheses as parts of ComplexFilter
        else:  # no operand found, end of input
            return a

    while text:
        # search F tokens
        f_match = re.match(
            rf'(?P<negate>~)?\s*(?P<fname>[\w -]+?)\s+(?P<fop>{"|".join(OP.keys())})\s+(?P<fvalue>\S+)(?<![,|&])', text
        )
        if f_match:
            kwargs = {f"{f_match.group('fname')}__{f_match.group('fop')}": f_match.group("fvalue")}
            if f_match.group("negate"):
                f_token = ~F(**kwargs)
            else:
                f_token = F(**kwargs)
        else:
            raise ValueError(f"Couldn't parse '{text}'!")
        text = text[f_match.end() :].strip()
        if not text:
            return f_token
        # search list or complex filter ops
        op_match = re.match(rf"(?P<op>and|or|,)\s+", text)
        if op_match:
            op = {"and": "&&", "or": "||", ",": ","}.get(op_match.group("op"))
        else:
            raise ValueError(f"Couldn't parse '{text}'!")
        text = text[op_match.end() :].strip()
        f_token2 = text_to_filter(text)
        if isinstance(f_token2, ComplexFilter):
            # noinspection PyTypeChecker
            return ComplexFilter(f_token, op, f_token2)
        if isinstance(f_token2, FilterList) and f_token2.op == op:
            if op == ",":
                return f_token + f_token2
            elif op == "&&":
                return f_token & f_token2
            elif op == "||":
                return f_token | f_token2
            raise ValueError(f"Couldn't parse '{text}'!")
        elif isinstance(f_token2, FilterList):
            # noinspection PyTypeChecker
            return ComplexFilter(f_token, op, f_token2)
        if isinstance(f_token2, F):
            # noinspection PyTypeChecker
            return FilterList(f_token, f_token2, op=op)
