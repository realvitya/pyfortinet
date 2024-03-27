"""FMG API for humans"""
import logging
from inspect import isclass
from typing import Optional, Union, Any, Type, List

from more_itertools import first

from pyfortinet.exceptions import FMGException, FMGWrongRequestException
from pyfortinet.fmg_api import FMGObject, FMGExecObject, AnyFMGObject, GetOption
from pyfortinet.fmg_api.fmgbase import FMGBase, FMGResponse, auth_required
from pyfortinet.settings import FMGSettings
from pyfortinet.fmg_api.common import FILTER_TYPE

logger = logging.getLogger(__name__)


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
        super().__init__(settings, **kwargs)

    @staticmethod
    def _get_filter_list(filters: FILTER_TYPE = None):
        """Derive filter list for API call

        This method is used by other methods to easily generate the filter data structure

        Args:
            filters: F object or ComplexFilter (composite of F object results)
        """
        if filters:
            return filters.generate()
        return None

    @auth_required
    def get(
        self,
        request: Union[dict[str, Any], Type[FMGObject]],
        filters: FILTER_TYPE = None,
        scope: Optional[str] = None,
        fields: Optional[List[str]] = None,
        loadsub: bool = True,
        options: Optional[List[GetOption]] = None
    ) -> FMGResponse:
        """Get info from FMG

        Args:
            request: Get operation's data structure
            scope: Scope where the object is searched (defaults to FMG setting on connection)
            filters: Filter expression
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
        if issubclass(request, FMGObject):
            # derive url from current scope and adom
            if not scope:  # get adom from FMG settings
                scope = "global" if self._settings.adom == "global" else f"adom/{self._settings.adom}"
            else:  # user specified
                scope = "global" if scope == "global" else f"adom/{scope}"
            url = request._url.default.replace("{scope}", scope)
            if self._settings.adom != "global":
                url = url.replace("{adom}", f"/adom/{self._settings.adom}")
            else:
                url = url.replace("{adom}", "")

            api_request = {
                "loadsub": 1 if loadsub else 0,
            }

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
        else:
            result.data = {"error": f"Wrong type of request received: {request}"}
            result.status = 400
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
            result.data = api_result
            return result
        # No need for the following. Pydantic "alias" can be used to handle space or dash in keys!
        # converting API names to object names (replace '-' and ' ' -> _)
        # obj_model = [
        #     {key.replace("-", "_").replace(" ", "_"): value for key, value in data.items()}
        #     for data in api_result.get("data")
        # ]
        # construct object list
        objects = []
        for value in api_result.get("data"):
            objects.append(request(**value, scope=scope, fmg=self))
        result.data = objects
        result.success = True
        return result

    def add(self, request: Union[dict[str, str], FMGObject]) -> FMGResponse:
        """Add operation

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
        if isinstance(request, dict):  # dict input, low-level operation
            return super().add(request)

        elif isinstance(request, FMGObject):  # high-level operation
            request.fmg_scope = request.fmg_scope or self._settings.adom
            api_data = request.model_dump(by_alias=True, exclude_none=True)
            return super().add(request={"url": request.get_url, "data": api_data})
        else:
            response.data = {"error": f"Wrong type of request received: {request}"}
            response.status = 400
            logger.error(response.data["error"])
            if self._raise_on_error:
                raise FMGWrongRequestException(request)
            return response

    def delete(self, request: Union[dict[str, str], FMGObject]) -> FMGResponse:
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
        if isinstance(request, dict):  # JSON input, low-level operation
            return super().delete(request)

        elif isinstance(request, FMGObject):  # high-level operation
            request.fmg_scope = request.fmg_scope or self._settings.adom
            return super().delete({"url": f"{request.get_url}/{request.name}"})  # assume URL with name for del operation
        else:
            response.data = {"error": f"Wrong type of request received: {request}"}
            response.status = 400
            logger.error(response.data["error"])
            if self._raise_on_error:
                raise FMGWrongRequestException(request)
            return response

    def update(self, request: Union[dict[str, str], FMGObject]) -> FMGResponse:
        """Update operation

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
        if isinstance(request, dict):  # JSON input, low-level operation
            return super().update(request)
        elif isinstance(request, FMGObject):  # high-level operation
            request.fmg_scope = request.fmg_scope or self._settings.adom
            api_data = request.model_dump(by_alias=True, exclude_none=True)
            return super().update({"url": request.get_url, "data": api_data})
        else:
            response.data = {"error": f"Wrong type of request received: {request}"}
            response.status = 400
            logger.error(response.data["error"])
            if self._raise_on_error:
                raise FMGWrongRequestException(request)
            return response

    def set(self, request: Union[dict[str, str], FMGObject]) -> FMGResponse:
        """Set operation

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
        if isinstance(request, dict):  # JSON input, low-level operation
            return super().set(request)
        elif isinstance(request, FMGObject):  # high-level operation
            request.fmg_scope = request.fmg_scope or self._settings.adom
            api_data = request.model_dump(by_alias=True, exclude_none=True)
            return super().set({"url": request.get_url, "data": api_data})
        else:
            response.data = {"error": f"Wrong type of request received: {request}"}
            response.status = 400
            logger.error(response.data["error"])
            if self._raise_on_error:
                raise FMGWrongRequestException(request)
            return response

    def exec(self, request: Union[dict[str, str], FMGExecObject]) -> FMGResponse:
        """Execute on FMG"""
        if isinstance(request, dict):  # low-level operation
            return super().exec(request)
        elif isinstance(request, FMGExecObject):
            logger.info("requesting exec with high-level op to %s", request.get_url)
            request.fmg_scope = request.fmg_scope or self._settings.adom
            return super().exec({"url": request.get_url, "data": request.data})
        else:
            result = FMGResponse(fmg=self, data={"error": f"Wrong type of request received: {request}"}, status=400)
            logger.error(result.data["error"])
            return result

    def get_obj(self, obj: Union[Type[FMGObject], Type[FMGExecObject], AnyFMGObject], **kwargs) -> AnyFMGObject:
        """Get an object and tie it to this FMG

        Arguments:
            obj: Any type or instance of FMGObject or FMGExecObject

        Keyword Args:
            kwargs: fields for the new object initialization

        Returns:
            (AnyFMGObject): New object, tied to this FMG
        """
        if isinstance(obj, Union[FMGObject, FMGExecObject]):
            obj._fmg = self
            return obj
        elif isclass(obj) and issubclass(obj, Union[FMGObject, FMGExecObject]):
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
            return [adom.get("name") for adom in response.data.get("data")]
        return None
