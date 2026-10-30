"""Shared task response interpretation."""

TERMINAL_TASK_STATES = frozenset({"cancelled", "done", "error", "aborted", "to_continue", "unknown"})


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
