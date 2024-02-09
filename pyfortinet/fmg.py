"""FMG API for humans"""
from typing import Optional, List, Union

from pyfortinet.fmg_api.dvmbd import Device
from pyfortinet.fmgbase import FMGBase, FMGSettings, FMGResponse
from pyfortinet.fmg_api.common import FILTER_TYPE


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

    def get_adom_list(self, filters: FILTER_TYPE = None):
        """Gather adoms from FMG

        Args:
            filters: filter as list or F object

        Returns:
            list of adom strings or None in case of error
        """
        request = {
            "url": "/dvmdb/adom",
            "fields": ["name"]
        }
        if filters:
            request["filter"] = self._get_filter_list(filters)

        response: FMGResponse = self.get(request)
        if response.success:
            return [adom.get("name") for adom in response.data.get("data")]
        return None

    def get_devices(self, filters: FILTER_TYPE = None, obj: bool = True) -> Union[FMGResponse, List[Device], None]:
        """Get device list from FMG

        Args:
            filters: filter as list or F object
            obj: whether return object or dict

        Returns
            list of devices from FMG or None in case of error
        """
        if self._settings.adom == "global":
            url = "/dvmdb/device"
        else:
            url = f"/dvmdb/adom/{self._settings.adom}/device"

        request = {
            "url": url,
            # "fields": ["name", "conf_status", "conn_status", "db_status", "dev_status"],
            "loadsub": 1,  # gather vdoms, ha_slaves
        }
        if filters:
            request["filter"] = self._get_filter_list(filters)
        response = self.get(request)
        if response.success:
            if obj:
                devices = [Device(**data) for data in response.data.get("data")]
                return devices
            else:
                return response
        return None
