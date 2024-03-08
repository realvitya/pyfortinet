"""FMGBase connection"""
import functools
import logging
import re
import time
from copy import copy
from dataclasses import dataclass, field
from random import randint
from typing import Any, Callable, Optional, Union, List

import requests
from pydantic import SecretStr

from pyfortinet.exceptions import (
    FMGAuthenticationException,
    FMGException,
    FMGLockException,
    FMGLockNeededException,
    FMGTokenException,
    FMGUnhandledException,
    FMGInvalidDataException,
    FMGObjectAlreadyExistsException, FMGInvalidURL,
)
from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.task import Task
from pyfortinet.settings import FMGSettings

logger = logging.getLogger(__name__)


def auth_required(func: Callable) -> Callable:
    """Decorator to provide authentication for the method

    Args:
        func: function to handle authentication errors

    Returns:
        (Callable): function with authentication handling enabled
    """

    @functools.wraps(func)
    def auth_decorated(self: Union[dict, "FMGBase"] = None, *args, **kwargs):
        """method which needs authentication"""
        if not self._token:
            raise FMGTokenException("No token was obtained. Open connection first!")
        try:
            return func(self, *args, **kwargs)
        except FMGAuthenticationException as err:
            try:  # try again after refreshing token
                self._token = self._get_token()
                return func(self, *args, **kwargs)
            except FMGException as err2:
                raise err2 from err

    return auth_decorated


def lock(func: Callable) -> Callable:
    """Decorator to provide ADOM locking if needed

    Args:
        func: function to handle errors complaining about no locking

    Returns:
        (Callable): function with lock handling enabled
    """

    @functools.wraps(func)
    def lock_decorated(self: "FMGBase" = None, *args, **kwargs):
        """method which needs locking"""
        try:
            return func(self, *args, **kwargs)
        except FMGLockNeededException as err:
            try:  # try again after locking
                if not args:  # in case we got kwargs request
                    args = [kwargs.get("request")]
                    del kwargs["request"]
                # args[0] is the request dict or obj
                if isinstance(args[0], dict):
                    url = args[0].get("url")
                    adom_match = re.search(r"/(?P<adom>global|(?<=adom/)\w+)/", url)
                    if adom_match:
                        adom = adom_match.group("adom")
                    else:
                        raise FMGException(f"No ADOM found to lock in url '{url}'") from err
                else:
                    adom = args[0].scope
                if adom not in self.lock.locked_adoms:
                    self.lock(adom)
                else:  # ADOM already locked, do not try to lock it again
                    raise
                return func(self, *args, **kwargs)
            except FMGException as err2:
                raise err2 from err

    return lock_decorated


@dataclass
class FMGResponse:
    """Response to a request

    Attributes:
        data (dict|List[FMGObject]): response data
        status (int): status code
        success (bool): True on success
    """

    data: Union[dict, List[FMGObject]] = field(default_factory=dict)  # data got from FMG
    status: int = 0  # status code of the request
    success: bool = False  # True on successful request
    fmg: "FMGBase" = None

    def __bool__(self) -> bool:
        return self.success

    def first(self) -> Optional[Union[FMGObject, dict]]:
        """Return first data or None if result is empty"""
        if isinstance(self.data, dict):
            if isinstance(self.data.get("data"), list):
                return self.data.get("data")[0] if self.data.get("data") else None
            else:
                return self.data.get("data")
        elif isinstance(self.data, list):
            return self.data[0] if self.data[0] else None
        return None

    def wait_for_task(self, timeout: int = 60, callback: Callable[[int, int], None] = None):
        if not self.success or not self.fmg:
            return
        self.fmg.wait_for_task(self, timeout, callback)


class FMGLockContext:
    """Lock FMG workspace"""

    def __init__(self, fmg: "FMGBase"):
        self._fmg = fmg
        self._locked_adoms = set()
        self._uses_workspace = False
        self._uses_adoms = False

    @property
    def uses_workspace(self) -> bool:
        """returns workspace usage"""
        return self._uses_workspace

    @property
    def locked_adoms(self) -> set[str]:
        """returns locked adom set"""
        return self._locked_adoms

    def __call__(self, *adoms: str):
        self.check_mode()
        if self._uses_workspace:
            self.lock_adoms(*adoms)
        return self

    def check_mode(self):
        """Get workspace-mode from config"""
        url = "/cli/global/system/global"
        result = self._fmg.get({"url": url, "fields": ["workspace-mode", "adom-status"]})
        self._uses_workspace = result.data["data"].get("workspace-mode") != 0
        # self.uses_adoms = result.data["data"].get("adom-status") == 1

    def lock_adoms(self, *adoms: str) -> FMGResponse:
        """Lock adom list

        If no adom specified, global workspace will be locked

        Args:
            *adoms (str): list of adom names

        Returns:
            Response object
        """
        result = FMGResponse(fmg=self._fmg)
        if not adoms:
            adoms = ["root"]
        for adom in adoms:
            url = "/dvmdb/global/workspace/lock/" if adom.lower() == "global" else f"/dvmdb/adom/{adom}/workspace/lock/"
            result.data.update({adom: self._fmg.exec(request={"url": url})})
            if result.data[adom].data.get("error"):
                raise FMGLockException(result.data[adom].data)
            self._locked_adoms.add(adom)
        return result

    def unlock_adoms(self, *adoms) -> FMGResponse:
        """unlock ADOMs"""
        result = FMGResponse(fmg=self._fmg)
        if not adoms:
            adoms = copy(self._locked_adoms)
        for adom in adoms:
            if adom.lower() == "global":
                url = "/dvmdb/global/workspace/unlock/"
            else:
                url = f"/dvmdb/adom/{adom}/workspace/unlock/"
            result.data.update({adom: self._fmg.exec(request={"url": url})})
            if not result.data[adom].data.get("error"):
                self._locked_adoms.remove(adom)

        if self._locked_adoms:
            raise FMGException(f"Failed to unlock ADOMs: {self._locked_adoms}")
        return result

    def commit_changes(self, adoms: Optional[list] = None, aux: bool = False) -> list[FMGResponse]:
        """Apply workspace changes in the DB

        Args:
            adoms: list of ADOMs to commit. If empty, commit ALL ADOMs.
            aux:

        Returns:
            (list[FMGResponse]): List of response of operations
        """
        results = []
        if not adoms:
            adoms = self._locked_adoms
        for adom in adoms:
            if aux:
                url = f"/pm/config/adom/{adom}/workspace/commit"
            elif adom.lower() == "global":
                url = "/dvmdb/global/workspace/commit/"
            else:
                url = f"/dvmdb/adom/{adom}/workspace/commit"
            results.append(self._fmg.exec({"url": url}))
        return results


class FMGBase:
    """Fortimanager connection class

    This can be used as a connection handler for the FortiManager. It maintains state of operation and provides
    functions to communicate with the FMG.

    Attributes:
        lock (FMGLockContext): Workspace lock handler

    Examples:
        Possible arguments to initialize: [FMGSettings](settings.md#settings.FMGSettings)

        ### Using as context manager

        >>> settings = {...}
        >>> with FMGBase(**settings) as conn:
        ...     print(conn.get_version())

        ### Using as function:

        >>> from pyfortinet.exceptions import FMGException
        >>> settings = {...}
        >>> conn = FMGBase(**settings)
        >>> try:
        ...     conn.open()
        ...     print(conn.get_version())
        ... except FMGException as err:
        ...     print(f"Error: {err}")
        ... finally:
        ...     conn.close()
    """

    def __init__(self, settings: Optional[FMGSettings] = None, **kwargs):
        """Initializes FMGBase

        Args:
            settings (Settings): FortiManager settings

        Keyword Args:
            base_url (str): Base URL to access FMG (e.g.: https://myfmg/jsonrpc)
            username (str): User to authenticate
            password (str): Password for authentication
            adom (str): ADOM to use for this connection
            verify (bool): Verify SSL certificate (REQUESTS_CA_BUNDLE can set accepted CA cert)
            timeout (float): Connection timeout for requests in seconds
            raise_on_error (bool): Raise exception on error
            discard_on_close (bool): Discard changes after connection close (workspace mode)
            discard_on_error (bool): Discard changes when exception occurs (workspace mode)
        """
        if not settings:
            settings = FMGSettings(**kwargs)
        self._settings = settings
        self._token: Optional[SecretStr] = None
        self._session: Optional[requests.Session] = None
        self.lock = FMGLockContext(self)
        self._raise_on_error: bool = settings.raise_on_error
        self._id: int = randint(1, 256)  # pick a random id for this session (check logs for a particular session)

    @property
    def adom(self) -> str:
        """Returns current selected adom"""
        return self._settings.adom

    @adom.setter
    def adom(self, adom: str) -> None:
        self._settings.adom = adom

    @property
    def discard_on_close(self) -> bool:
        """Returns discard_on_close value"""
        return self._settings.discard_on_close

    @discard_on_close.setter
    def discard_on_close(self, setting: bool) -> None:
        self._settings.discard_on_close = bool(setting)

    @property
    def raise_on_error(self):
        """Returns raise_on_error value"""
        return self._raise_on_error

    @raise_on_error.setter
    def raise_on_error(self, value: bool):
        self._raise_on_error = bool(value)

    def open(self) -> "FMGBase":
        """open connection"""
        logger.debug("Initializing connection to %s with id: %s", self._settings.base_url, self._id)
        self._session = requests.Session()
        self._token = self._get_token()
        return self

    def close(self, discard_changes: bool = False):
        """close connection"""
        # Logout and expire token
        request = {
            "id": self._id,
            "method": "exec",
            "params": [{"url": "/sys/logout"}],
            "session": self._token.get_secret_value(),
        }
        self._settings.discard_on_close = self._settings.discard_on_close or discard_changes
        try:
            try:
                if self.lock.uses_workspace:
                    if not self.discard_on_close:
                        self.lock.commit_changes()
                    self.lock.unlock_adoms()
            except FMGException:  # go ahead and ensure logout regardless we could unlock
                pass
            req = self._session.post(
                self._settings.base_url, json=request, verify=self._settings.verify, timeout=self._settings.timeout
            )
            status = req.json().get("result", [{}])[0].get("status", {})
            if status.get("code") != 0:
                logger.warning("Logout failed!")
        except requests.exceptions.ConnectionError:
            logger.warning("Logout failed!")

        self._session.close()
        self._token = None
        logger.debug("Closed session")

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is not None:
            self.close(discard_changes=self._settings.discard_on_error or self._settings.discard_on_close)
            return
        self.close(discard_changes=self.discard_on_close)

    def _post(self, request: dict) -> Any:
        logger.debug("posting data: %s", request)
        req = self._session.post(
            self._settings.base_url, json=request, verify=self._settings.verify, timeout=self._settings.timeout
        )
        results = req.json().get("result", [])
        for result in results:
            status = result["status"]
            if status["code"] == 0:
                continue
            if status["message"] == "no write permission":
                raise FMGLockNeededException(status)
            if status["message"] == "Workspace is locked by other user":
                raise FMGLockException(status)
            if status["message"] == "No permission for the resource":
                raise FMGAuthenticationException(status)
            if status["message"] == "The data is invalid for selected url":
                raise FMGInvalidDataException(status)
            if status["message"] == "Object already exists":
                raise FMGObjectAlreadyExistsException(f"{status}: {request.get('params')}")
            if status["message"] == "Invalid url":
                raise FMGInvalidURL(f"URL: {request['params'][0]['url']}")
            raise FMGUnhandledException(status)
        return results[0] if len(results) == 1 else results

    def _get_token(self) -> SecretStr:
        """Get authentication token

        Raises:
            (FMGTokenException): upon problem getting the token
        """
        logger.debug("Getting token..")
        request = {
            "id": self._id,
            "method": "exec",
            "params": [
                {
                    "data": {"passwd": self._settings.password.get_secret_value(), "user": self._settings.username},
                    "url": "/sys/login/user",
                }
            ],
        }
        try:
            req = self._session.post(self._settings.base_url, json=request, verify=self._settings.verify)
            status = req.json().get("result", [{}])[0].get("status", {})
            if status.get("code") != 0:
                if "No permission for resource" in status.get("message"):
                    raise FMGUnhandledException("No permission for resource, probably user does not have API access!")
                raise FMGTokenException("Login failed, wrong credentials!")
            logger.debug("Token obtained")
        except FMGTokenException as err:
            logger.error("Can't gather token: %s", err)
            raise err
        except requests.exceptions.ConnectionError as err:
            logger.error("Can't gather token: %s", err)
            raise err
        token = req.json().get("session", "")
        return SecretStr(token)

    @auth_required
    def get_version(self) -> str:
        """Gather FMG version"""
        request = {
            "method": "get",
            "params": [{"url": "/sys/status"}],
            "id": self._id,
            "session": self._token.get_secret_value(),
        }
        req = self._post(request)
        return req["data"]["Version"]

    @auth_required
    def exec(self, request: dict[str, str]) -> FMGResponse:
        """Execute on FMG"""
        logger.info("requesting exec with low-level op to %s", request.get("url"))
        body = {
            "method": "exec",
            "params": [
                {
                    "data": request.get("data"),
                    "url": request.get("url"),
                }
            ],
            "session": self._token.get_secret_value(),
            "id": self._id,
        }
        try:
            api_result = self._post(request=body)
        except FMGException as err:
            api_result = {"error": str(err)}
            logger.error("Error in exec request: %s", api_result["error"])
        result = FMGResponse(fmg=self, data=api_result, success=api_result.get("status", {}).get("code") == 0)
        return result

    # noqa: PLR0912 - Too many branches
    @auth_required
    def get(self, request: dict[str, Any]) -> FMGResponse:  # noqa: PLR0912 - Too many branches
        """Get info from FMG

        Args:
            request: Get operation's param structure

        Examples:
            ## Low-level - dict

            >>> address_request = {
            ...    "url": "/pm/config/global/obj/firewall/address",
            ...    "filter": [ ["name", "==", "test-address"] ],
            ...    "fields": [ "name", "subnet" ]
            ...}
            >>> settings = {...}
            >>> with FMGBase(**settings) as fmg:
            ...    fmg.get(address_request)

        Returns:
            (FMGResponse): response object with data
        """
        body = {
            "method": "get",
            "params": [request],
            "session": self._token.get_secret_value(),
            "id": self._id,
        }
        result = FMGResponse(fmg=self)
        try:
            api_result = self._post(request=body)
        except FMGException as err:
            api_result = {"error": str(err)}
            logger.error("Error in get request: %s", api_result["error"])
            if self._raise_on_error:
                raise
            result.data = api_result
            return result
        # handling empty result list
        if not api_result.get("data"):
            result.data = {"data": []}
            return result
        # processing result list
        result.data = api_result
        result.success = True
        result.status = api_result.get("status", {}).get("code", 400)

        return result

    @auth_required
    @lock
    def add(self, request: dict[str, str]) -> FMGResponse:
        """Add operation

        Args:
            request: Add operation's data structure

        Examples:
            >>> settings = {...}
            >>> address_request = {
            ...     "url": "/pm/config/global/obj/firewall/address",
            ...     "data": {
            ...         "name": "test-address",
            ...         "associated-interface": "inside",
            ...         "obj-type": "ip",
            ...         "type": "ipmask",
            ...         "start-ip": "10.0.0.1/24"
            ...     }
            ... }
            >>> with FMGBase(**settings) as fmg:
            >>>     fmg.add(address_request)

        Returns:
            (FMGResponse): Result of operation
        """
        response = FMGResponse(fmg=self)
        body = {
            "method": "add",
            "params": [
                {
                    "data": request.get("data"),
                    "url": request.get("url"),
                }
            ],
            "session": self._token.get_secret_value(),
            "id": self._id,
        }
        try:
            api_result = self._post(request=body)
            response.success = True
            response.status = api_result.get("status")
        except FMGUnhandledException as err:
            api_result = {"error": str(err)}
            logger.error("Error in add request: %s", api_result["error"])
            if self._raise_on_error:
                raise
        response.data = api_result
        return response

    @auth_required
    @lock
    def update(self, request: dict[str, str]) -> FMGResponse:
        """Update operation

        Args:
            request: Update operation's data structure

        Examples:
            >>> settings = {...}
            >>> address_request = {
            ...     "url": "/pm/config/global/obj/firewall/address",
            ...     "data": {
            ...         "name": "test-address",
            ...         "associated-interface": "inside",
            ...         "obj-type": "ip",
            ...         "type": "ipmask",
            ...         "start-ip": "10.0.0.1/24"
            ...     }
            ... }
            >>> with FMGBase(**settings) as fmg:
            >>>     fmg.update(address_request)

        Returns:
            (FMGResponse): Result of operation
        """
        response = FMGResponse(fmg=self)
        body = {
            "method": "update",
            "params": [
                {
                    "data": request.get("data"),
                    "url": request.get("url"),
                }
            ],
            "session": self._token.get_secret_value(),
            "id": self._id,
        }
        try:
            api_result = self._post(request=body)
            response.success = True
            response.status = api_result.get("status")
        except FMGUnhandledException as err:
            api_result = {"error": str(err)}
            logger.error("Error in update request: %s", api_result["error"])
            if self._raise_on_error:
                raise
        response.data = api_result
        return response

    @auth_required
    @lock
    def set(self, request: dict[str, str]) -> FMGResponse:
        """Set operation

        Args:
            request: Set operation's data structure

        Examples:
            >>> settings = {...}
            >>> address_request = {
            ...     "url": "/pm/config/global/obj/firewall/address",
            ...     "data": {
            ...         "name": "test-address",
            ...         "associated-interface": "inside",
            ...         "obj-type": "ip",
            ...         "type": "ipmask",
            ...         "start-ip": "10.0.0.1/24"
            ...     }
            ... }
            >>> with FMGBase(**settings) as fmg:
            >>>     fmg.set(address_request)

        Returns:
            (FMGResponse): Result of operation
        """
        response = FMGResponse(fmg=self)
        body = {
            "method": "set",
            "params": [
                {
                    "data": request.get("data"),
                    "url": request.get("url"),
                }
            ],
            "session": self._token.get_secret_value(),
            "id": self._id,
        }
        try:
            api_result = self._post(request=body)
            response.success = True
            response.status = api_result.get("status")
        except FMGUnhandledException as err:
            api_result = {"error": str(err)}
            logger.error("Error in update request: %s", api_result["error"])
            if self._raise_on_error:
                raise
        response.data = api_result
        return response

    @auth_required
    @lock
    def delete(self, request: dict[str, str]) -> FMGResponse:
        """Delete operation

        Args:
            request: Update operation's data structure

        Examples:
            ## Low-level - dict

            >>> settings = {...}
            >>> address_request = {
            ...     "url": "/pm/config/global/obj/firewall/address/test-address",
            ... }
            >>> with FMGBase(**settings) as fmg:
            >>>     fmg.delete(address_request)

        Returns:
            (FMGResponse): Result of operation
        """
        response = FMGResponse(fmg=self)
        body = {
            "method": "delete",
            "params": [
                {
                    "url": request.get("url"),
                }
            ],
            "session": self._token.get_secret_value(),
            "id": self._id,
        }
        try:
            api_result = self._post(request=body)
            response.success = True
            response.status = api_result.get("status")
        except FMGUnhandledException as err:
            api_result = {"error": str(err)}
            logger.error("Error in get request: %s", api_result["error"])
            if self._raise_on_error:
                raise
        response.data = api_result
        return response

    def wait_for_task(
        self, task_res: Union[int, FMGResponse], timeout: int = 60, callback: Callable[[int], None] = None
    ) -> Union[str, None]:
        """Wait for task to finish

        Args: task_res: (int, FMGResponse): Task or task ID to check
        timeout: (int): timeout for waiting
        callback: (Callable[[int], None]): function to call in each iteration.
                                           It must accept 1 arg which is the current percentage

        Example:
            >>> from pyfortinet.fmg_api.dvmcmd import Device, DeviceTask
            >>> from rich.progress import Progress
            >>> settings = {...}
            >>> device = Device(name="test", ip="1.1.1.1", adm_usr="test", adm_pass="<PASSWORD>")
            >>> with FMGBase(**settings) as fmg:
            ...     task = DeviceTask(adom=fmg.adom, device=device)
            ...     result = fmg.exec(task)
            ...     with Progress() as progress:
            ...         prog_task = progress.add_task(f"Adding device {device.name}", total=100)
            ...         update_progress = lambda percent: progress.update(prog_task, percent)
            ...         task.wait_for_task(task, callback=update_progress)
        """
        task_id = task_res if isinstance(task_res, int) else task_res.data.get("data", {}).get("taskid")
        if task_id is None:
            return
        start_time = time.time()
        while True:
            task = self.get(Task, F(id=task_id))
            task_data: Task = task.first()
            if not task.success:
                return
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Timed out waiting {timeout} seconds for the task {task.id}!")
            if callback:
                callback(task_data.percent)
            # exit on the following states
            if task_data.state in ["cancelled", "done", "error", "aborted", "to_continue", "unknown"]:
                return task_data.state
            time.sleep(5)
