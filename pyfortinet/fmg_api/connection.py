"""FMG connection"""
import functools
import logging
import re
from copy import copy
from dataclasses import dataclass, field
from typing import Any, Optional, Union, List, Dict

import requests
from more_itertools import first
from pydantic import SecretStr

from pyfortinet.fmg_api import FMGObject, FMGExecObject

# from pyfortinet.fmg_api.exceptions import FMGException, FMGTokenException, FMGAuthenticationException, \
#     FMGLockNeededException
import pyfortinet.fmg_api.exceptions as fe
from pyfortinet.fmg_api.settings import FMGSettings

logger = logging.getLogger(__name__)


def auth_required(func):
    """Decorator to provide authentication for the method

    Args:
        func: function to handle authentication errors

    Returns:
        function with authentication handling enabled
    """

    @functools.wraps(func)
    def auth_decorated(self, *args, **kwargs):
        """method which needs authentication"""
        if not self._token:
            raise fe.FMGTokenException("No token was obtained. Open connection first!")
        try:
            return func(self, *args, **kwargs)
        except fe.FMGAuthenticationException as err:
            try:  # try again after refreshing token
                self._token = self._get_token()  # pylint: disable=protected-access  # decorator of methods
                return func(self, *args, **kwargs)
            except fe.FMGException as err2:
                raise err2 from err

    return auth_decorated


def lock(func):
    """Decorator to provide ADOM locking if needed

    Args:
        func: function to handle errors complaining about no locking

    Returns:
        function with lock handling enabled
    """

    @functools.wraps(func)
    def lock_decorated(self, *args, **kwargs):
        """method which needs locking"""
        try:
            return func(self, *args, **kwargs)
        except fe.FMGLockNeededException as err:
            try:  # try again after locking
                # args[0] is the request dict or obj
                # url = args[0].get("url") if isinstance(args[0], dict) else args[0].url
                if isinstance(args[0], dict):
                    url = args[0].get("url")
                    adom_match = re.search(r"/(?P<adom>global|(?<=adom/)\w+)/", url)
                    if adom_match:
                        adom = adom_match.group("adom")
                    else:
                        raise fe.FMGException(f"No ADOM found to lock in url '{url}'") from err
                else:
                    adom = args[0].scope
                if adom not in self.lock.locked_adoms:
                    self.lock(adom)
                else:  # ADOM already locked, do not try to lock it again
                    raise
                return func(self, *args, **kwargs)
            except fe.FMGException as err2:
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
    def locked_adoms(self):
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

    def lock_adoms(self, *adoms) -> FMGResponse:
        """Lock adom list

        If no adom specified, global workspace will be locked

        Args:
            *adoms: list of adom names

        Returns:
            Response object
        """
        result = FMGResponse()
        if not adoms:
            adoms = ["root"]
        for adom in adoms:
            if adom.lower() == "global":
                url = "/dvmdb/global/workspace/lock/"
            else:
                url = f"/dvmdb/adom/{adom}/workspace/lock/"
            result.data.update({adom: self._fmg.exec(request={"url": url})})
            if result.data[adom].data.get("error"):
                raise fe.FMGLockException(result.data[adom].data)
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
            result.data.update({adom: self._fmg.exec({"url": url})})
            if not result.data[adom].data.get("error"):
                self._locked_adoms.remove(adom)

        if self._locked_adoms:
            raise fe.FMGException(f"Failed to unlock ADOMs: {self._locked_adoms}")
        return result

    def commit_changes(self, adoms: Optional[list] = None, aux: bool = False) -> List[FMGResponse]:
        """Apply workspace changes in the DB

        Args:
            adoms: list of ADOMs to commit. If empty, commit ALL ADOMs.
            aux:
        """
        results = []
        if not adoms:
            adoms = self._locked_adoms
        for adom in adoms:
            if aux:
                url = f"/pm/config/adom/{adom}/workspace/commit"
            else:
                if adom.lower() == "global":
                    url = "/dvmdb/global/workspace/commit/"
                else:
                    url = f"/dvmdb/adom/{adom}/workspace/commit"
            results.append(self._fmg.exec({"url": url}))
        return results


class FMG:
    """Fortimanager connection class

    Attributes:
        lock: Workspace lock handler
    """

    def __init__(self, settings: FMGSettings):
        logger.debug("Initializing connection to %s", settings.base_url)
        self._settings = settings
        self._token: Optional[SecretStr] = None
        self._session: Optional[requests.Session] = None
        self.lock = FMGLockContext(self)
        self._raise_on_error: bool = settings.raise_on_error
        self._discard_on_close: bool = False

    def open(self) -> "FMG":
        """open connection"""
        self._session = requests.Session()
        self._token = self._get_token()
        return self

    def close(self, discard_changes: bool = False):
        """close connection"""
        # Logout and expire token
        request = {
            "id": 1,
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
            except fe.FMGException:  # go ahead and ensure logout regardless we could unlock
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
                raise fe.FMGLockNeededException(status)
            if status["message"] == "Workspace is locked by other user":
                raise fe.FMGLockException(status)
            raise fe.FMGUnhandledException(status)
        return results[0] if len(results) == 1 else results

    def _get_token(self) -> SecretStr:
        """Get authentication token

        Raises:

        """
        logger.debug("Getting token..")
        request = {
            "id": 1,
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
                raise fe.FMGTokenException("Login failed, wrong credentials!")
            logger.debug("Token obtained")
        except fe.FMGTokenException as err:
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
            "id": 1,
            "session": self._token.get_secret_value(),
        }
        req = self._post(request)
        return req["data"]["Version"]

    @auth_required
    def exec(self, request: Union[Dict[str, str], FMGObject]) -> FMGResponse:
        """Execute on FMG"""
        if isinstance(request, dict):  # lowlevel operation
            logger.info("requesting exec with lowlevel op to %s", request.get("url"))
            body = {
                "method": "exec",
                "params": [
                    {
                        "data": request.get("data"),
                        "url": request.get("url"),
                    }
                ],
                "session": self._token.get_secret_value(),
                "id": 1,
            }
            try:
                api_result = self._post(request=body)
            except fe.FMGException as err:
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
                "id": 1,
            }
            try:
                api_result = self._post(request=body)
            except fe.FMGException as err:
                api_result = {"error": str(err)}
                logger.error("Error in get request: %s", api_result["error"])
            result = FMGResponse(data=api_result)
        else:
            result = FMGResponse(data={"error": f"Wrong type of request received: {request}"}, status=400)
            logger.error(result.data["error"])

        return result

    @auth_required
    def get(self, request: Union[Dict[str, Any], FMGObject]) -> Union[FMGResponse, FMGObject, List[FMGObject]]:
        """Get info from FMG

        Args:
            request: Get operation's data structure

        Examples:
            .. code-block::

                1. dict - lowlevel
                address_request = {
                    "url": "/pm/config/global/obj/firewall/address",
                    "filter": [ ["name", "==", "test-address"] ],
                    "fields": [ "name", "subnet" ]
                }
                with FMG(settings) as fmg:
                    fmg.add(address_request)

                2. FMGObject - highlevel
                address = Address(name="test-address")
                with FMG(settings) as fmg:
                    address = fmg.get(address)

        Returns:
            (FMGResponse): response object with data
            (FMGObject): if request was an object, it will return a filled object
        """
        if isinstance(request, dict):  # low-level operation
            body = {
                "method": "get",
                "params": [request],
                "session": self._token.get_secret_value(),
                "id": 1,
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
            scope = "global" if request.scope == "global" else f"adom/{request.scope}"
            url = request.url.replace("{scope}", scope)
            body = {
                "method": "get",
                "params": [{"url": url, **api_request}],
                "session": self._token.get_secret_value(),
                "id": 1,
            }
        else:
            result = FMGResponse(data={"error": f"Wrong type of request received: {request}"}, status=400)
            logger.error(result.data["error"])
            if self._raise_on_error:
                raise fe.FMGWrongRequestException(result)
            return result
        try:
            api_result = self._post(request=body)
        except fe.FMGException as err:
            api_result = {"error": str(err)}
            logger.error("Error in get request: %s", api_result["error"])
            if self._raise_on_error:
                raise
            return FMGResponse(data=api_result)
        # handling empty result list
        if not api_result.get("data"):
            if self._raise_on_error:
                raise fe.FMGEmptyResultException(request)
            return FMGResponse(data=request)
        # processing result list
        if isinstance(request, dict):
            result = FMGResponse(data=api_result)
            result.success = True
        else:
            # converting API names to object names (replace - -> _)
            obj_model = [{key.replace("-", "_"): value for key, value in data.items()} for data in api_result.get("data")]
            if len(obj_model) > 1:
                result = []
                for value in obj_model:
                    result.append(type(request)(**value))
            else:
                result = type(request)(**first(obj_model))

        return result

    @auth_required
    @lock
    def add(self, request: Union[Dict[str, str], FMGObject]) -> FMGResponse:
        """Add operation

        Args:
            request: Add operation's data structure

        Examples:
            .. code-block::

                1. dict - lowlevel
                address_request = {
                    "url": "/pm/config/global/obj/firewall/address",
                    "data": {
                        "name": "test-address",
                        "associated-interface": "inside",
                        "obj-type": "ip",
                        "type": "ipmask",
                        "start-ip": "10.0.0.1/24"
                    }
                }
                with FMG(settings) as fmg:
                    fmg.add(address_request)

                2. Address - highlevel
                address = Address(name="test-address", associated-interface="inside", obj_type="ip",
                                  type="ipmask", start_ip="10.0.0.1/24")
                with FMG(settings) as fmg:
                    fmg.add(address)
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
                "id": 1,
            }
        elif isinstance(request, FMGObject):  # high-level operation
            api_data = {
                key: value
                for key, value in request.model_dump(by_alias=True).items()
                if not key.startswith("_") and value is not None
            }
            scope = "global" if request.scope == "global" else f"adom/{request.scope}"
            url = request.url.replace("{scope}", scope)
            body = {
                "method": "add",
                "params": [{"url": url, "data": api_data}],
                "session": self._token.get_secret_value(),
                "id": 1,
            }
        else:
            response.data = {"error": f"Wrong type of request received: {request}"}
            response.status = 400
            logger.error(response.data["error"])
            if self._raise_on_error:
                raise fe.FMGWrongRequestException(request)
            return response
        try:
            api_result = self._post(request=body)
            response.success = True
            response.status = api_result.get("status")
        except fe.FMGUnhandledException as err:
            api_result = {"error": str(err)}
            logger.error("Error in get request: %s", api_result["error"])
            if self._raise_on_error:
                raise
        response.data = api_result
        return response
