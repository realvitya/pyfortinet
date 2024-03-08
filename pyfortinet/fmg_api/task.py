"""Task"""
from typing import Literal, Optional, Union, List

from pydantic import Field, field_validator, model_validator

from pyfortinet.fmg_api import FMGExecObject, FMGObject


class TaskLineHistory(FMGObject):
    """Task line history"""

    detail: str
    name: str
    percent: int
    vdom: Optional[str] = None


TASK_SRC = Literal[
    "device manager",
    "security console",
    "global object",
    "config installation",
    "script installation",
    "check point",
    "import objects",
    "import interfaces and zones",
    "import policy",
    "ems policy",
    "policy check",
    "assignment",
    "object assignment",
    "cloning package",
    "certificate enrollment",
    "install objects",
    "unknown",
    "install device",
    "fwm",
    "integrity check",
    "cloning policy block",
    "import config",
    "generate controllers",
]

TASK_STATE = Literal[
    "pending",
    "running",
    "cancelling",
    "cancelled",
    "done",
    "error",
    "aborting",
    "aborted",
    "warning",
    "to_continue",
    "unknown",
]


class TaskLine(FMGObject):
    """Task line object"""

    detail: str
    end_tm: Optional[int] = 0
    err: Optional[int] = 0
    history: Optional[List[TaskLineHistory]]
    ip: Optional[str] = None
    name: str
    oid: Optional[int] = 0
    percent: Optional[int] = 0
    start_tm: Optional[int] = 0
    state: TASK_STATE
    vdom: Optional[str] = None

    @field_validator("state", mode="before")
    def validate_src(cls, v: int) -> TASK_STATE:
        return TASK_STATE.__dict__.get("__args__")[v]


class Task(FMGObject):
    """Task class"""
    _url = "/task/task"

    adom: Optional[int]
    end_tm: Optional[int]
    flags: Optional[int]
    id: Optional[int]
    line: Optional[List[TaskLine]]
    num_done: Optional[int] = 0
    num_err: Optional[int] = 0
    num_lines: Optional[int] = 0
    num_warn: Optional[int] = 0
    percent: Optional[int] = 0
    pid: Optional[int] = 0
    src: TASK_SRC = "device manager"
    start_tm: Optional[int] = 0
    state: TASK_STATE = "pending"
    title: str = ""
    tot_percent: Optional[int] = 0
    user: str = ""

    @field_validator("src", mode="before")
    def validate_src(cls, v: int) -> TASK_SRC:
        return TASK_SRC.__dict__.get("__args__")[v]

    @field_validator("state", mode="before")
    def validate_state(cls, v: int) -> TASK_STATE:
        return TASK_STATE.__dict__.get("__args__")[v]
