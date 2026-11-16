# Tasks and installation

Task creation, polling, and inspection are distinct steps. Use an open connection as described
in the [object guide](index.md), and keep it open until an operation has finished.

## InstallDeviceTask

`InstallDeviceTask` installs device settings from FortiManager onto explicitly selected devices.
It is not a policy-package installation wrapper. Review pending configuration before execution:
installation may apply changes made outside your script.

```python
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.securityconsole import InstallDeviceTask

install = fmg.get_obj(
    InstallDeviceTask,
    adom=fmg.adom,
    scope=[Scope(name="branch-fw", vdom="root")],
    flags=["auto_lock_ws"],
)
response = install.exec()
state = response.wait_for_task(callback=lambda percent, log: print(percent, log))
if state != "done":
    raise RuntimeError(f"Installation did not complete successfully: {state}")
```

The device and VDOM must exist. With an asynchronous client, await `install.exec()` and
`response.wait_for_task()`. A successful execution response does not establish successful
installation. Missing task metadata or an unsuccessful status read can produce `None`;
other terminal states also need application handling.

## Task

`Task` represents task status returned by FortiManager. Read it by filtering the collection:

```python
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.task import Task

task = fmg.get(Task, F(id=123)).first()
if task is not None:
    print(task.id, task.state, task.percent, task.num_err)
```

Replace `123` with a task ID returned by an actual operation. The model has required response
fields, so `Task(id=123)` is not a minimal lookup model; use the class and an `F` filter.

If the ID is already available, polling also works directly:

```python
state = fmg.wait_for_task(123)
```

The low-level clients support this polling helper too. See
[advanced usage](../advanced_usage.md#waiting_for_tasks) for callback and failure behavior.

## TaskLine and TaskLineHistory

`TaskLine` and `TaskLineHistory` describe nested task details. They do not define independent
resource URLs. Inspect them through a `Task` response:

```python
if task is not None:
    for line in task.line or []:
        print(line.name, line.state, line.percent, line.detail)
        for entry in line.history or []:
            print(entry.name, entry.vdom, entry.percent, entry.detail)
```

These are status records, not task-creation objects. A terminal state other than `done`,
errors in task lines, or an unsuccessful lookup should be handled explicitly by the application.
