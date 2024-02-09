"""Task"""
from typing import Literal, Optional, Union, List

from pydantic import Field, field_validator, model_validator

from pyfortinet.fmg_api import FMGExecObject, FMGObject
from pyfortinet.fmg_api.common import BaseDevice, Scope, OS_VER, OS_TYPE, MGMT_MODE


class TaskLineHistory(FMGObject):
    """Task line history"""

    detail: str
    name: str
    percent: int
    vdom: str


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
    ip: str
    name: str
    oid: Optional[int] = 0
    percent: Optional[int] = 0
    start_tm: Optional[int] = 0
    state: TASK_STATE
    vdom: str


class Task(FMGObject):
    """Task class"""

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
