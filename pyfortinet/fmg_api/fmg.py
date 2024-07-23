"""FMG API for humans"""

import logging
import re
from inspect import isclass
from typing import Optional, Union, Any, Type, List, Dict

from more_itertools import first

from pyfortinet.exceptions import FMGException, FMGWrongRequestException, FMGMissingMasterKeyException
from pyfortinet.fmg_api import FMGObject, FMGExecObject, AnyFMGObject, GetOption
from pyfortinet.fmg_api.fmgbase import FMGBase, FMGResponse, auth_required
from pyfortinet.settings import FMGSettings
from pyfortinet.fmg_api.common import FILTER_TYPE, F, text_to_filter

logger = logging.getLogger(__name__)

REQUEST_ARG = Union[dict[str, Any], FMGObject]
MULTI_REQUEST_ARG = Union[REQUEST_ARG, List[REQUEST_ARG]]


class FMG(FMGBase):
    """FMG API for humans

    Goal of this class to provide easy access to FMG features. This extends the base class capabilities with easy to use
    methods.
    """

    def __init__(self, settings: Optional[FMGSettings] = None, **kwargs):
        """Initializes FMG

        Args:
            settings (Settings): FortiManager settings

        Keyword Args:
            base_url (str): Base URL to access FMG (e.g.: https://myfmg)
            username (str): User to authenticate
            password (str): Password for authentication
            adom (str): ADOM to use for this connection
            verify (bool): Verify SSL certificate (REQUESTS_CA_BUNDLE can set accepted CA cert)
            timeout (float): Connection timeout for requests in seconds
            raise_on_error (bool): Raise exception on error
            discard_on_close (bool): Discard changes after connection close (workspace mode)
            discard_on_error (bool): Discard changes when exception occurs (workspace mode)
        """
        super().__init__(settings, **kwargs)

    @staticmethod
    def _get_filter_list(filters: FILTER_TYPE = None):
        """Derive filter list for API call

        This method is used by other methods to easily generate the filter data structure

        Args:
            filters: F object or ComplexFilter (composite of F object results)
        """
        if filters:
            if isinstance(filters, FILTER_TYPE):
                return filters.generate()
            elif isinstance(filters, str):
                return text_to_filter(filters).generate()
        return None

    @auth_required
    def get(
        self,
        request: Union[dict[str, Any], FMGObject, Type[FMGObject]],
        filters: Union[str, FILTER_TYPE] = None,
        scope: Optional[str] = None,
        fields: Optional[List[str]] = None,
        loadsub: bool = True,
        options: Optional[List[GetOption]] = None,
    ) -> FMGResponse:
        """Get info from FMG

        If `request` is an `FMGObject` instance, it's initialized values will be considered as filters!

        Args:
            request: Get operation's data structure
            scope: Scope where the object is searched (defaults to FMG setting on connection)
            filters: Filter expression as text or using `F`
            fields: Fields to return (default: None means all fields)
            loadsub: Load sub objects
            options: API request options

        Examples:
            ## Low-level - dict

            ```pycon

            >>> address_request = {
            ...    "url": "/pm/config/global/obj/firewall/address",
            ...    "filter": [ ["name", "==", "test-address"] ],
            ...    "fields": [ "name", "subnet" ]
            ...}
            >>> settings = {...}
            >>> with FMG(**settings) as fmg:
            ...    fmg.get(address_request)
            ```

            ## High-level - obj

            ```pycon

            >>> from pyfortinet.fmg_api.firewall import Address
            >>> from pyfortinet.fmg_api.common import F
            >>> settings = {...}
            >>> with FMG(**settings) as fmg:
            ...    addresses = fmg.get(Address, F(name__like="test-%") & F(subnet="test-subnet"))
            ```

        Returns:
            (FMGResponse): response object with data
        """
        # Call base function for base arguments
        if isinstance(request, dict):
            return super().get(request)
        # High level arguments
        result = FMGResponse(fmg=self)
        api_request = {
            "loadsub": 1 if loadsub else 0,
        }
        if isinstance(request, FMGObject):
            # derive url from current scope and adom
            if not request.fmg_scope:  # assign local FMG scope to request as fallback
                request.fmg_scope = scope or self.adom
            url = request.get_url
            for field in request.model_dump(by_alias=True, exclude_none=True):
                if filters:
                    filters &= F(**{field: getattr(request, field.replace(" ", "_").replace("-", "_"))})
                else:
                    filters = F(**{field: getattr(request, field.replace(" ", "_").replace("-", "_"))})
        elif issubclass(request, FMGObject):
            # pydantic model default value
            url = request._url.default
            # remove /{field} parts except scope
            # reason: there are urls with specific parameters which we can't provide with using class
            # this way, we can cover some cases where general list of objects will return when there is no specific
            # parameter. Such a request is `dynamic.Interface`
            # Use object instance instead, where URL processing is done by the object's `get_url` property!
            url = re.sub(r"/{(?!scope).*?}", "", url)
            # derive url from current scope and adom
            if not scope:  # get adom from FMG settings
                scope = "global" if self.adom == "global" else f"adom/{self.adom}"
            else:  # user specified
                scope = "global" if scope == "global" else f"adom/{scope}"
            url = url.replace("{scope}", scope)
        else:
            result.data = {"error": f"Wrong type of request received: {request}"}
            result.status = 400
            logger.error(result.data["error"])
            if self._raise_on_error:
                raise FMGWrongRequestException(result)
            return result

        if filters:
            api_request["filter"] = self._get_filter_list(filters)

        if options:
            api_request["option"] = options

        body = {
            "method": "get",
            "params": [{"url": url, **api_request}],
            "verbose": 1,
            "session": self._token.get_secret_value(),
            "id": self._id,
        }

        try:
            api_result = self._post(request=body)
        except FMGException as err:
            api_result = {"error": str(err)}
            logger.error("Error in get request: %s", api_result["error"])
            if self._raise_on_error:
                raise
            result.data = api_result
            return result
        # construct object list
        objects = []
        obj_class = type(request) if isinstance(request, FMGObject) else request
        for value in api_result.get("data"):
            objects.append(obj_class(**value, fmg_scope=scope, fmg=self))
        result.data = objects
        result.success = True
        return result

    def add(self, request: MULTI_REQUEST_ARG) -> FMGResponse:
        """Add operation

        Notes:
            This method supports passing multiple objects as list

        Args:
            request: Add operation's data structure or object

        Examples:
            ## Low-level - dict

            ```pycon

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
            ...     fmg.add(address_request)
            ```

            ## High-level - obj

            ```pycon

            >>> from pyfortinet.fmg_api.firewall import Address
            >>> settings = {...}
            >>> address = Address(name="test-address", associated_interface="inside", obj_type="ip",
            ...                   type="ipmask", start_ip="10.0.0.1/24")
            >>> with FMG(**settings) as fmg:
            ...     fmg.add(address)
            ```

        Returns:
            (FMGResponse): Result of operation
        """
        response = FMGResponse(fmg=self)
        if not isinstance(request, list):
            request = [request]
        if isinstance(request[0], dict):  # dict input, low-level operation
            return super().add(request)
        elif isinstance(request[0], FMGObject):  # high-level operation
            api_data = []
            for req in request:
                req.fmg_scope = req.fmg_scope or self._settings.adom
                api_data.append({"url": req.get_url, "data": req.model_dump(by_alias=True, exclude_none=True)})
            return super().add(request=api_data)
        else:
            response.data = {"error": f"Wrong type of request received: {request}"}
            logger.error(response.data["error"])
            if self._raise_on_error:
                raise FMGWrongRequestException(request)
            return response

    def delete(self, request: MULTI_REQUEST_ARG) -> FMGResponse:
        """Delete operation

        Args:
            request: dict or object to delete

        Examples:
            ## Low-level - dict

            ```pycon

            >>> settings = {...}
            >>> address_request = {
            ...     "url": "/pm/config/global/obj/firewall/address/test-address",
            ... }
            >>> with FMG(**settings) as fmg:
            ...     fmg.delete(address_request)
            ```

            ## High-level - obj

            ```pycon

            >>> from pyfortinet.fmg_api.firewall import Address
            >>> settings = {...}
            >>> address = Address(name="test-address")
            >>> with FMG(**settings) as fmg:
            ...     fmg.delete(address)
            ```

        Returns:
            (FMGResponse): Result of operation
        """
        response = FMGResponse(fmg=self)
        if not isinstance(request, list):
            request = [request]
        if isinstance(request[0], dict):  # dict input, low-level operation
            return super().delete(request)

        elif isinstance(request[0], FMGObject):  # high-level operation
            api_data = []
            for req in request:
                req.fmg_scope = req.fmg_scope or self._settings.adom
                if not req.master_keys:
                    raise FMGMissingMasterKeyException(f"Need to specify a master key for {request}")
                master_key = first(req.master_keys)  # assume one master_key, like `name`
                master_value = getattr(req, master_key)
                api_data.append({"url": f"{req.get_url}/{master_value}"})
            return super().delete(api_data)
        else:
            response.data = {"error": f"Wrong type of request received: {request}"}
            logger.error(response.data["error"])
            if self._raise_on_error:
                raise FMGWrongRequestException(request)
            return response

    def update(self, request: MULTI_REQUEST_ARG) -> FMGResponse:
        """Update operation

        Notes:
            This method supports passing multiple objects as list

        Args:
            request: Update operation's data structure

        Examples:
            ## Low-level - dict

            ```pycon

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
            ...     fmg.update(address_request)
            ```

            ## High-level - obj

            ```pycon

            >>> from pyfortinet.fmg_api.firewall import Address
            >>> settings = {...}
            >>> address = Address(name="test-address", associated_interface="inside", obj_type="ip",
            ...                   type="ipmask", start_ip="10.0.0.1/24")
            >>> with FMGBase(**settings) as fmg:
            ...     fmg.update(address)
            ```

        Returns:
            (FMGResponse): Result of operation
        """
        response = FMGResponse(fmg=self)
        if not isinstance(request, list):
            request = [request]
        if isinstance(request[0], dict):  # dict input, low-level operation
            return super().update(request)
        elif isinstance(request[0], FMGObject):  # high-level operation
            api_data = []
            for req in request:
                req.fmg_scope = req.fmg_scope or self._settings.adom
                api_data.append({"url": req.get_url, "data": req.model_dump(by_alias=True, exclude_none=True)})
            return super().update(request=api_data)

        else:
            response.data = {"error": f"Wrong type of request received: {request}"}
            logger.error(response.data["error"])
            if self._raise_on_error:
                raise FMGWrongRequestException(request)
            return response

    def set(self, request: MULTI_REQUEST_ARG) -> FMGResponse:
        """Set operation

        Notes:
            This method supports passing multiple objects as list

        Args:
            request: Update operation's data structure

        Examples:
            ## Low-level - dict

            ```pycon

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
            ...     fmg.set(address_request)
            ```

            ## High-level - obj

            ```pycon

            >>> from pyfortinet.fmg_api.firewall import Address
            >>> settings = {...}
            >>> address = Address(name="test-address", associated_interface="inside", obj_type="ip",
            ...                   type="ipmask", start_ip="10.0.0.1/24")
            >>> with FMGBase(**settings) as fmg:
            ...     fmg.set(address)
            ```

        Returns:
            (FMGResponse): Result of operation
        """
        response = FMGResponse(fmg=self)
        if not isinstance(request, list):
            request = [request]
        if isinstance(request[0], dict):  # dict input, low-level operation
            return super().set(request)
        elif isinstance(request[0], FMGObject):  # high-level operation
            api_data = []
            for req in request:
                req.fmg_scope = req.fmg_scope or self._settings.adom
                api_data.append({"url": req.get_url, "data": req.model_dump(by_alias=True, exclude_none=True)})
            return super().set(request=api_data)

        else:
            response.data = [{"error": f"Wrong type of request received: {request}"}]
            logger.error(response.data[0]["error"])
            if self._raise_on_error:
                raise FMGWrongRequestException(request)
            return response

    def exec(self, request: Union[dict[str, Any], FMGExecObject]) -> FMGResponse:
        """Execute on FMG"""
        if isinstance(request, dict):  # low-level operation
            return super().exec(request)
        elif isinstance(request, FMGExecObject):
            logger.info("requesting exec with high-level op to %s", request.get_url)
            request.fmg_scope = request.fmg_scope or self._settings.adom
            return super().exec({"url": request.get_url, "data": request.data})
        else:
            result = FMGResponse(fmg=self, data=[{"error": f"Wrong type of request received: {request}"}])
            logger.error(result.data[0]["error"])
            return result

    def get_obj(
        self, obj: Union[Type[FMGObject], Type[FMGExecObject], AnyFMGObject], **kwargs: Any
    ) -> AnyFMGObject:
        """Get an object and tie it to this FMG

        Arguments:
            obj: Any type or instance of FMGObject or FMGExecObject

        Keyword Args:
            kwargs: fields for the new object initialization

        Returns:
            (AnyFMGObject): New object, tied to this FMG
        """
        if isinstance(obj, (FMGObject, FMGExecObject)):
            obj._fmg = self
            return obj
        elif isclass(obj) and issubclass(obj, (FMGObject, FMGExecObject)):
            return obj(fmg=self, **kwargs)

        raise TypeError(f"Argument {obj} is not an FMGObject or FMGExecObject type")

    def get_adom_list(self, filters: FILTER_TYPE = None) -> Optional[List[str]]:
        """Gather adoms from FMG

        Args:
            filters: filter as list or F object

        Returns:
            list of adom strings or None in case of error
        """
        request = {"url": "/dvmdb/adom", "fields": ["name"]}
        if filters:
            request["filter"] = self._get_filter_list(filters)

        response: FMGResponse = self.get(request)
        if response.success:
            return [adom.get("name") for adom in response.data[0].get("data")]
        return None

    def refresh(self, obj: FMGObject) -> FMGObject:
        """Re-load data from FMG"""
        if not obj.master_keys:
            raise FMGMissingMasterKeyException
        # Build filter
        filter_complex = F(**{obj.master_keys[0]: getattr(obj, obj.master_keys[0])})
        for f in obj.master_keys[1:]:
            filter_complex = filter_complex & F(**{f: getattr(obj, f)})
        # Get object data, assume only one because we use master keys (primary key in sql)
        new = self.get(type(obj), filter_complex).first()
        if new:
            # overwrite our object fields with data from FMG
            for att in vars(obj):
                setattr(obj, att, getattr(new, att))
        return obj

    def clone(self, request: REQUEST_ARG, *, create_task: bool = False, **new: str) -> FMGResponse:
        """Clone an object

        Args:
            request (dict|FMGObject): Object to clone or request dict
            create_task (bool): Create background task and do not block here. Beware, that you must not close connection
                                till task is finished, otherwise the task might fail. (use wait_for_task)
            new (str): keys for new object

        Note:
            The object need to have _master_keys which is defining the base of cloning. Usually it's "name", but
            it is possible to define multiple master keys for future use. All those will be passed to the API.

            This method does NOT support multiple requests in one call! Use low-level API if this is needed!

        Example:
            ## Low-level - dict

            ```pycon

            >>> settings = {...}
            >>> clone_request = {
            ...     "url": "/pm/config/global/obj/firewall/address/test-address",  # source object
            ...     "data": {
            ....         "name": "clone-address",  # destination object
            ... }
            >>> with FMGBase(**settings) as fmg:
            ...     fmg.clone(clone_request)
            ```

            ## High-level - obj

            ```pycon

            >>> from pyfortinet.fmg_api.dvmdb ADOM
            >>> adom = fmg.get_obj(ADOM(name="myadom"))  # source object
            >>> result = fmg.clone(adom, create_task=True, name="newadom")  # destination object
            >>> result.wait_for_task()
            "done"
            ```

        """
        response = FMGResponse(fmg=self)
        if isinstance(request, dict):  # JSON input, low-level operation
            return super().clone(request, create_task=create_task)
        elif isinstance(request, FMGObject):  # high-level operation
            if not request.master_keys:
                raise FMGMissingMasterKeyException(f"Need to specify a master key for {request}")
            master_key = first(request.master_keys)  # assume one master_key, like `name`
            master_value = getattr(request, master_key)
            request.fmg_scope = request.fmg_scope or self._settings.adom
            return super().clone(
                {
                    "url": f"{request.get_url}/{master_value}",
                    "data": new,
                },
                create_task=create_task,
            )
        else:
            response.data = {"error": f"Wrong type of request received: {request}"}
            response.status = 400
            logger.error(response.data["error"])
            if self._raise_on_error:
                raise FMGWrongRequestException(request)
            return response
