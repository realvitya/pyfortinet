"""FMG API for humans"""
import logging
from typing import Optional, Union, Any, Type

from more_itertools import first

from pyfortinet.exceptions import FMGException, FMGWrongRequestException, FMGEmptyResultException
from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmgbase import FMGBase, FMGSettings, FMGResponse
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

    def get(
        self,
        request: Union[dict[str, Any], FMGObject, Type[FMGObject]],
        filters: FILTER_TYPE = None,
        loadsub: bool = True,
    ) -> Union[FMGResponse, FMGObject, list[FMGObject]]:
        """Get info from FMG

        Args:
            request: Get operation's data structure
            filters: Override object or dict filters with filter expression
            loadsub: Load sub objects

        Examples:
            ## Low-level - dict

            >>> address_request = {
            ...    "url": "/pm/config/global/obj/firewall/address",
            ...    "filter": [ ["name", "==", "test-address"] ],
            ...    "fields": [ "name", "subnet" ]
            ...}
            >>> settings = {...}
            >>> with FMGBase(**settings) as fmg:
            ...    fmg.add(address_request)

            ## High-level - obj

            >>> from pyfortinet.fmg_api.firewall import Address
            >>> settings = {...}
            >>> address = Address(name="test-address")
            >>> with FMGBase(**settings) as fmg:
            ...    address = fmg.get(address)

            ## Advanced filtering

            >>> from pyfortinet.fmg_api.firewall import Address
            >>> from pyfortinet.fmg_api.common import F
            >>> settings = {...}
            >>> with FMGBase(**settings) as fmg:
            ...    addresses = fmg.get(Address, F(name__like="test-%") & F(subnet="test-subnet"))

        Returns:
            (FMGResponse): response object with data
            (FMGObject): if request was an object, it will return a filled object
            (list[FMGObject]): if more object returns, it will return a list of objects
        """
        # Call base function for base arguments
        if isinstance(request, dict) or isinstance(request, FMGObject):
            return super().get(request)
        # Advanced filtering
        if issubclass(request, FMGObject):
            scope = "global" if self._settings.adom == "global" else f"adom/{self._settings.adom}"
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

            body = {
                "method": "get",
                "params": [{"url": url, **api_request}],
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
            return FMGResponse(data=body)
        # converting API names to object names (replace '-' and ' ' -> _)
        obj_model = [
            {key.replace("-", "_").replace(" ", "_"): value for key, value in data.items()}
            for data in api_result.get("data")
        ]
        if len(obj_model) > 1:
            result = []
            for value in obj_model:
                result.append(request(**value))
        else:
            result = request(**first(obj_model))
        return result

    def get_adom_list(self, filters: FILTER_TYPE = None):
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
