"""FMG connection"""
import functools
import logging
import re
from copy import copy
from dataclasses import dataclass, field
from random import randint
from typing import Any, Callable, Optional, Union

import requests
from more_itertools import first
from pydantic import SecretStr

from pyfortinet import FMGSettings
from pyfortinet.exceptions import (
    FMGAuthenticationException,
    FMGEmptyResultException,
    FMGException,
    FMGLockException,
    FMGLockNeededException,
    FMGTokenException,
    FMGUnhandledException,
    FMGWrongRequestException,
)
from pyfortinet.fmg_api import FMGExecObject, FMGObject

logger = logging.getLogger(__name__)


def auth_required(func: Callable) -> Callable:
    """Decorator to provide authentication for the method

    Args:
        func: function to handle authentication errors

    Returns:
        (Callable): function with authentication handling enabled
    """

    @functools.wraps(func)
    def auth_decorated(self: Union[dict, "FMG"] = None, *args, **kwargs):
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
    def lock_decorated(self: Union[dict, "FMG"] = None, *args, **kwargs):
        """method which needs locking"""
        try:
            return func(self, *args, **kwargs)
        except FMGLockNeededException as err:
            try:  # try again after locking
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
    """Response to a request"""

    data: dict = field(default_factory=dict)  # data got from FMG
    status: int = 0  # status code of the request
    success: bool = False  # True on successful request


class FMGLockContext:
    """Lock FMG workspace"""

    def __init__(self, fmg: "FMG"):
        self._fmg = fmg
        self._locked_adoms = set()
        self._uses_workspace = False
        self._uses_adoms = False

    @property
    def uses_workspace(self) -> bool:
        """returns workspace usage"""
        return self._uses_workspace

    # @uses_workspace.setter
    # def uses_workspace(self, val: bool):
    #     self._uses_workspace = val

    # @property
    # def uses_adoms(self) -> bool:
    #     return self._uses_adoms
    #
    # @uses_adoms.setter
    # def uses_adoms(self, val: bool):
    #     self._uses_adoms = val

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
        result = FMGResponse()
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
        result = FMGResponse()
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


class FMG:
    """Fortimanager connection class

    This can be used as a connection handler for the FortiManager. It maintains state of operation and provides
    functions to communicate with the FMG.

    Attributes:
        lock (FMGLockContext): Workspace lock handler

    Examples:
        Possible arguments to initialize: [FMGSettings](settings.md#settings.FMGSettings)

        ### Using as context manager

        >>> settings = {...}
        >>> with FMG(**settings) as conn:
        ...     print(conn.get_version())

        ### Using as function:

        >>> from pyfortinet.exceptions import FMGException
        >>> settings = {...}
        >>> conn = FMG(**settings)
        >>> try:
        ...     conn.open()
        ...     print(conn.get_version())
        ... except FMGException as err:
        ...     print(f"Error: {err}")
        ... finally:
        ...     conn.close()
    """

    def __init__(self, settings: Optional[FMGSettings] = None, **kwargs):
        if not settings:
            settings = FMGSettings(**kwargs)
        self._settings = settings
        self._token: Optional[SecretStr] = None
        self._session: Optional[requests.Session] = None
        self.lock = FMGLockContext(self)
        self._raise_on_error: bool = settings.raise_on_error
        self._discard_on_close: bool = False
        self._id: int = randint(1, 256)  # pick a random id for this session (check logs for a particular session)

    def open(self) -> "FMG":
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
        self._discard_on_close = self._discard_on_close or discard_changes
        try:
            try:
                if self.lock.uses_workspace:
                    if not self._discard_on_close:
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
        self.close()

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
    def exec(self, request: Union[dict[str, str], FMGObject]) -> FMGResponse:
        """Execute on FMG"""
        if isinstance(request, dict):  # low-level operation
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
                logger.error("Error in get request: %s", api_result["error"])
            result = FMGResponse(data=api_result)
        elif isinstance(request, FMGExecObject):
            logger.info("requesting exec with high-level op to %s", request.url)
            body = {
                "method": "exec",
                "params": [
                    {
                        "data": request.data,
                        "url": request.url,
                    }
                ],
                "session": self._token.get_secret_value(),
                "id": self._id,
            }
            try:
                api_result = self._post(request=body)
            except FMGException as err:
                api_result = {"error": str(err)}
                logger.error("Error in get request: %s", api_result["error"])
            result = FMGResponse(data=api_result)
        else:
            result = FMGResponse(data={"error": f"Wrong type of request received: {request}"}, status=400)
            logger.error(result.data["error"])

        return result

    # noqa: PLR0912 - Too many branches
    @auth_required
    def get(self, request: Union[dict[str, Any], FMGObject]) -> Union[FMGResponse, FMGObject, list[FMGObject]]:  # noqa: PLR0912 - Too many branches
        """Get info from FMG

        Args:
            request: Get operation's data structure

        Examples:
            ## Low-level - dict

            >>> address_request = {
            ...    "url": "/pm/config/global/obj/firewall/address",
            ...    "filter": [ ["name", "==", "test-address"] ],
            ...    "fields": [ "name", "subnet" ]
            ...}
            >>> settings = {...}
            >>> with FMG(**settings) as fmg:
            ...    fmg.add(address_request)

            ## High-level - obj

            >>> from pyfortinet.fmg_api.firewall import Address
            >>> settings = {...}
            >>> address = Address(name="test-address")
            >>> with FMG(**settings) as fmg:
            ...    address = fmg.get(address)

        Returns:
            (FMGResponse): response object with data
            (FMGObject): if request was an object, it will return a filled object
            (list[FMGObject]): if more object returns, it will return a list of objects
        """
        if isinstance(request, dict):  # low-level operation
            body = {
                "method": "get",
                "params": [request],
                "session": self._token.get_secret_value(),
                "id": self._id,
            }
        elif isinstance(request, FMGObject):  # high-level operation
            api_request = {
                "filter": [
                    [key, "==", value]
                    for key, value in request.model_dump(by_alias=True).items()
                    if not key.startswith("_") and value is not None
                ],
                "fields": list(request.model_dump(by_alias=True).keys()),
            }
            body = {
                "method": "get",
                "params": [{"url": request.url, **api_request}],
                "session": self._token.get_secret_value(),
                "id": self._id,
            }
        else:
            result = FMGResponse(data={"error": f"Wrong type of request received: {request}"}, status=400)
            logger.error(result.data["error"])
            if self._raise_on_error:
                raise FMGWrongRequestException(result)
            return result
        try:
            api_result = self._post(request=body)
        except FMGException as err:
            api_result = {"error": str(err)}
            logger.error("Error in get request: %s", api_result["error"])
            if self._raise_on_error:
                raise
            return FMGResponse(data=api_result)
        # handling empty result list
        if not api_result.get("data"):
            if self._raise_on_error:
                raise FMGEmptyResultException(request)
            return FMGResponse(data=request)
        # processing result list
        if isinstance(request, dict):
            result = FMGResponse(data=api_result)
            result.success = True
        else:
            # converting API names to object names (replace '-' and ' ' -> _)
            obj_model = [
                {key.replace("-", "_").replace(" ", "_"): value for key, value in data.items()}
                for data in api_result.get("data")
            ]
            if len(obj_model) > 1:
                result = []
                for value in obj_model:
                    result.append(type(request)(**value))
            else:
                result = type(request)(**first(obj_model))

        return result

    @auth_required
    @lock
    def add(self, request: Union[dict[str, str], FMGObject]) -> FMGResponse:
        """Add operation

        Args:
            request: Add operation's data structure

        Examples:
            ## Low-level - dict

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
            >>> with FMG(**settings) as fmg:
            >>>     fmg.add(address_request)

            ## High-level - obj

            >>> from pyfortinet.fmg_api.firewall import Address
            >>> settings = {...}
            >>> address = Address(name="test-address", associated_interface="inside", obj_type="ip",
            ...                   type="ipmask", start_ip="10.0.0.1/24")
            >>> with FMG(**settings) as fmg:
            ...     fmg.add(address)

        Returns:
            (FMGResponse): Result of operation
        """
        response = FMGResponse()
        if isinstance(request, dict):  # JSON input, low-level operation
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
        elif isinstance(request, FMGObject):  # high-level operation
            api_data = {
                key: value
                for key, value in request.model_dump(by_alias=True).items()
                if not key.startswith("_") and value is not None
            }
            body = {
                "method": "add",
                "params": [{"url": request.url, "data": api_data}],
                "session": self._token.get_secret_value(),
                "id": self._id,
            }
        else:
            response.data = {"error": f"Wrong type of request received: {request}"}
            response.status = 400
            logger.error(response.data["error"])
            if self._raise_on_error:
                raise FMGWrongRequestException(request)
            return response
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
