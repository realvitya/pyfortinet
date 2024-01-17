"""FMG API for humans"""
from typing import Union

from pyfortinet.fmg import FMG, FMGSettings, FMGResponse
from pyfortinet.fmg_api.common import F, ComplexFilter


class FMGHL(FMG):
    """FMG API for humans

    Goal of this class to provide easy access to FMG features. This extends the base class capabilities with easy to use
    methods.
    """
    @staticmethod
    def _get_filter_list(filters: Union[F, ComplexFilter] = None):
        """Derive filter list for API call

        This method is used by other methods to easily generate the filter data structure

        Args:
            filters: F object or ComplexFilter (composite of F object results)
        """
        if filters:
            return filters.generate()
        return None

    def get_adom_list(self, filters: Union[F, ComplexFilter] = None):
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
