"""Shared task response interpretation."""

from pyfortinet.fmg_api.task import Task

TERMINAL_TASK_STATES = frozenset({"cancelled", "done", "error", "aborted", "warning", "to_continue", "unknown"})


def task_id_from_response(response):
    """Read either task identifier spelling returned by FortiManager."""
    if isinstance(response, int):
        return response
    if not response.success:
        return None
    data = response.data
    if isinstance(data, list):
        data = data[0] if data else {}
    data = data.get("data") if isinstance(data, dict) else None
    if not isinstance(data, dict):
        return None
    task_id = data.get("taskid")
    return task_id if task_id is not None else data.get("task")


def task_from_response(response):
    """Decode a task from a successful low-level GET result."""
    if not response.success:
        return None
    result = response.first()
    if result is None:
        return None
    data = result.get("data")
    if isinstance(data, list):
        data = data[0] if data else None
    return Task(**data) if data is not None else None
