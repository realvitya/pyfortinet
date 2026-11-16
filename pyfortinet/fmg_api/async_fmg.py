"""High-level FortiManager object API."""

import logging
from inspect import isclass
from typing import Optional, Union, Any, Type, List, Dict

from more_itertools import first

from pyfortinet.fmg_api.async_fmgbase import AsyncFMGBase, AsyncFMGResponse, auth_required, error_handling
from pyfortinet.exceptions import (
    FMGException,
    FMGWrongRequestException,
    FMGMissingMasterKeyException,
    FMGObjectNotExistException,
)
from pyfortinet.fmg_api import FMGObject, FMGExecObject, AnyFMGObject, GetOption
from pyfortinet.settings import FMGSettings
from pyfortinet.fmg_api.common import FILTER_TYPE, F, text_to_filter, FilterList, ComplexFilter
from pyfortinet.fmg_api._requests import prepare_batch, prepare_get, prepare_refresh, response_url_fields

logger = logging.getLogger(__name__)

REQUEST_ARG = Union[dict[str, Any], FMGObject]
MULTI_REQUEST_ARG = Union[REQUEST_ARG, List[REQUEST_ARG]]


class AsyncFMG(AsyncFMGBase):
    """High-level asynchronous FortiManager client.

    Accepts configuration models and execution objects, constructs API requests, and returns
    bound models from high-level GET operations. Dictionary requests remain supported for
    endpoints without models. Use an authenticated connection context for object operations.

    Install the async extra and await requests and operations on bound objects.
    Constructing or binding an object with get_obj() does not require awaiting.
    """

    def __init__(self, settings: Optional[FMGSettings] = None, **kwargs):
        """Initialize the FortiManager client

        Args:
            settings (FMGSettings): Connection settings; when supplied, takes precedence over keyword settings

        Keyword Args:
            base_url (str): Base URL to access FMG (e.g.: https://myfmg)
            username (str): User to authenticate
            password (str): Password for authentication
            adom (str): ADOM to use for this connection
            verify (bool): Verify SSL certificate (REQUESTS_CA_BUNDLE can set accepted CA cert)
            timeout (float): Connect/read inactivity timeout per transport attempt, in seconds
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
            if isinstance(filters, (F, FilterList, ComplexFilter)):
                return filters.generate()
            elif isinstance(filters, str):
                return text_to_filter(filters).generate()
        return None

    @error_handling
    @auth_required
    async def get(
        self,
        request: Union[dict[str, Any], FMGObject, Type[FMGObject]],
        filters: Union[str, FILTER_TYPE] = None,
        scope: Optional[str] = None,
        fields: Optional[List[str]] = None,
        loadsub: bool = True,
        options: Optional[List[GetOption]] = None,
        **kwargs: Optional[Dict[str, str]],
    ) -> AsyncFMGResponse:
        """Read objects from FortiManager.

        Args:
            request: Model class for a collection, initialized model for selection, or raw request dictionary.
            filters: Filter expression as text or composed with F.
            scope: Request scope; an explicit model scope takes precedence.
            fields: API field names to request, or None for all fields.
            loadsub: Request nested tables.
            options: Additional API GET options.

        Returns:
            AsyncFMGResponse: High-level data contains bound models. A successful empty lookup
            has an empty data list and first() returns None. Dictionary requests retain raw results.

        Examples:
            Use configured connection settings and handle an empty lookup:

            ```python
            from pyfortinet import AsyncFMG
            from pyfortinet.fmg_api.common import F
            from pyfortinet.fmg_api.firewall import Address

            async with AsyncFMG(**config) as fmg:
                response = await fmg.get(Address, F(name__like="server%"))
                for address in response.data:
                    print(address.name, address.subnet)
                server = (await fmg.get(Address(name="server1"))).first()
                if server is not None:
                    print(server.name)
            ```
        """
        # Call base function for base arguments
        if isinstance(request, dict):
            return await super().get(request)
        # High level arguments
        result = AsyncFMGResponse(fmg=self)
        api_request, object_scope = prepare_get(
            request, self.adom, filters=filters, scope=scope, fields=fields, loadsub=loadsub, options=options
        )

        body = {
            "method": "get",
            "params": [api_request],
            "verbose": 1,
            "session": self._token.get_secret_value(),
            "id": self._id,
        }

        try:
            api_result = await self._post(request=body)
        except FMGObjectNotExistException:
            api_result = {"data": []}

        # construct object list
        objects = []
        obj_class = type(request) if isinstance(request, FMGObject) else request
        url_fields = response_url_fields(request)
        values = api_result.get("data")
        if values is None:
            values = []
        elif not isinstance(values, list):
            values = [values]
        for value in values:
            objects.append(obj_class(**{**url_fields, **value}, fmg_scope=object_scope, fmg=self))
        result.data = objects
        result.success = True
        return result

    @error_handling
    async def add(self, request: MULTI_REQUEST_ARG) -> AsyncFMGResponse:
        """Create configuration objects in FortiManager.

        Args:
            request: One model or dictionary, or a nonempty list containing only models or only dictionaries.

        Returns:
            AsyncFMGResponse: Operation status; read the object separately to obtain its resulting configuration.

        Notes:
            This operation writes configuration. Models use API aliases and omit None values.
            Empty lists are sent explicitly. Batch operations are not a transaction; partial writes
            may remain after a failure. Check firmware semantics before using SET for a resource.

        Examples:
            Inside an open connection, with the appropriate target and permissions:

            ```python
            from pyfortinet.fmg_api.firewall import Address

            address = Address(name="example-server", subnet="192.0.2.10/32")
            response = await fmg.add(address)
            ```
        """
        request = prepare_batch(request, allow_objects=True)
        if isinstance(request[0], dict):  # dict input, low-level operation
            return await super().add(request)

        elif isinstance(request[0], FMGObject):  # high-level operation
            api_data = []
            for req in request:
                req.fmg_scope = req.fmg_scope or self._settings.adom
                api_data.append(
                    {"url": req.get_url(method="add"), "data": req.model_dump(by_alias=True, exclude_none=True)}
                )
            return await super().add(request=api_data)

    @error_handling
    async def delete(self, request: MULTI_REQUEST_ARG) -> AsyncFMGResponse:
        """Delete the identified configuration objects.

        Args:
            request: One model or dictionary, or a nonempty list containing only models or only dictionaries.

        Returns:
            AsyncFMGResponse: Operation status; read the object separately to obtain its resulting configuration.

        Notes:
            This operation writes configuration. Models use API aliases and omit None values.
            Empty lists are sent explicitly. Batch operations are not a transaction; partial writes
            may remain after a failure. Check firmware semantics before using SET for a resource.

        Examples:
            Inside an open connection, with the appropriate target and permissions:

            ```python
            from pyfortinet.fmg_api.firewall import Address

            address = Address(name="example-server")
            response = await fmg.delete(address)
            ```
        """
        request = prepare_batch(request, allow_objects=True)
        if isinstance(request[0], dict):  # dict input, low-level operation
            return await super().delete(request)

        elif isinstance(request[0], FMGObject):  # high-level operation
            api_data = []
            for req in request:
                req.fmg_scope = req.fmg_scope or self._settings.adom
                api_data.append({"url": req.get_url(method="delete")})
            return await super().delete(api_data)

    @error_handling
    async def update(self, request: MULTI_REQUEST_ARG) -> AsyncFMGResponse:
        """Update supplied non-null configuration fields.

        Args:
            request: One model or dictionary, or a nonempty list containing only models or only dictionaries.

        Returns:
            AsyncFMGResponse: Operation status; read the object separately to obtain its resulting configuration.

        Notes:
            This operation writes configuration. Models use API aliases and omit None values.
            Empty lists are sent explicitly. Batch operations are not a transaction; partial writes
            may remain after a failure. Check firmware semantics before using SET for a resource.

        Examples:
            Inside an open connection, with the appropriate target and permissions:

            ```python
            from pyfortinet.fmg_api.firewall import Address

            address = Address(name="example-server", comment="Application server")
            response = await fmg.update(address)
            ```
        """
        request = prepare_batch(request, allow_objects=True)
        if isinstance(request[0], dict):  # dict input, low-level operation
            return await super().update(request)

        elif isinstance(request[0], FMGObject):  # high-level operation
            api_data = []
            for req in request:
                req.fmg_scope = req.fmg_scope or self._settings.adom
                api_data.append(
                    {"url": req.get_url(method="update"), "data": req.model_dump(by_alias=True, exclude_none=True)}
                )
            return await super().update(request=api_data)

    @error_handling
    async def set(self, request: MULTI_REQUEST_ARG) -> AsyncFMGResponse:
        """Submit a FortiManager SET operation for the supplied objects.

        Args:
            request: One model or dictionary, or a nonempty list containing only models or only dictionaries.

        Returns:
            AsyncFMGResponse: Operation status; read the object separately to obtain its resulting configuration.

        Notes:
            This operation writes configuration. Models use API aliases and omit None values.
            Empty lists are sent explicitly. Batch operations are not a transaction; partial writes
            may remain after a failure. Check firmware semantics before using SET for a resource.

        Examples:
            Inside an open connection, with the appropriate target and permissions:

            ```python
            from pyfortinet.fmg_api.firewall import Address

            address = Address(name="example-server", subnet="192.0.2.10/32")
            response = await fmg.set(address)
            ```
        """
        request = prepare_batch(request, allow_objects=True)
        if isinstance(request[0], dict):  # dict input, low-level operation
            return await super().set(request)

        elif isinstance(request[0], FMGObject):  # high-level operation
            api_data = []
            for req in request:
                req.fmg_scope = req.fmg_scope or self._settings.adom
                api_data.append(
                    {"url": req.get_url(method="set"), "data": req.model_dump(by_alias=True, exclude_none=True)}
                )
            return await super().set(request=api_data)

    async def exec(self, request: Union[dict[str, Any], FMGExecObject]) -> AsyncFMGResponse:
        """Execute on FMG"""
        if isinstance(request, dict):  # low-level operation
            return await super().exec(request)
        elif isinstance(request, FMGExecObject):
            logger.info("requesting exec with high-level op to %s", request.get_url())
            request.fmg_scope = request.fmg_scope or self._settings.adom
            return await super().exec({"url": request.get_url(), "data": request.data})
        else:
            result = AsyncFMGResponse(fmg=self, data=[{"error": f"Wrong type of request received: {request}"}])
            logger.error(result.data[0]["error"])
            if self._raise_on_error:
                raise FMGWrongRequestException(result.data[0]["error"])
            return result

    def get_obj(self, obj: Union[Type[FMGObject], Type[FMGExecObject], AnyFMGObject], **kwargs: Any) -> AnyFMGObject:
        """Construct or bind a local model to this client without an API request.

        Args:
            obj: FMGObject or FMGExecObject class, or an existing instance.
            **kwargs: Initialization fields when obj is a class; ignored for existing instances.

        Returns:
            AnyFMGObject: A new instance for a class argument, or the same bound instance for an object argument.

        Examples:
            This method is synchronous for both clients. Creating the model does not create the remote object:

            ```python
            from pyfortinet.fmg_api.firewall import Address

            address = fmg.get_obj(Address, name="example-server", subnet="192.0.2.10/32")
            ```
        """
        if isinstance(obj, (FMGObject, FMGExecObject)):
            obj._fmg = self
            return obj
        elif isclass(obj) and issubclass(obj, (FMGObject, FMGExecObject)):
            return obj(fmg=self, **kwargs)

        raise TypeError(f"Argument {obj} is not an FMGObject or FMGExecObject type")

    async def get_adom_list(self, filters: FILTER_TYPE = None) -> Optional[List[str]]:
        """Gather adoms from FMG

        Args:
            filters: filter as list or F object

        Returns:
            list of adom strings or None in case of error
        """
        request = {"url": "/dvmdb/adom", "fields": ["name"]}
        if filters:
            request["filter"] = self._get_filter_list(filters)

        response: AsyncFMGResponse = await self.get(request)
        if response.success:
            return [adom.get("name") for adom in response.data[0].get("data")]
        return None

    async def refresh(self, obj: FMGObject) -> FMGObject:
        """Re-load data from FMG"""
        if not obj.master_keys:
            raise FMGMissingMasterKeyException
        # Use master key fields only to identify this object, filters are not appropriate as there might be URL
        # fields amongst master keys
        new = await self.get(prepare_refresh(obj))
        if not new.success:
            raise FMGWrongRequestException("Cannot refresh object because the lookup failed")
        if len(new.data) != 1:
            raise FMGWrongRequestException(
                f"{obj} need to load from FMG first in order to call .refresh()!",
            )
        new = new.first()
        if new:
            # overwrite our object fields with data from FMG
            for att, definition in type(obj).model_fields.items():
                if not definition.exclude:  # excluded fields should not be overwritten (e.g. URL fields)
                    setattr(obj, att, getattr(new, att))
        return obj

    async def clone(self, request: REQUEST_ARG, *, create_task: bool = False, **new: str) -> AsyncFMGResponse:
        """Clone one configuration object using new identity values.

        Args:
            request: Source model or raw clone request dictionary.
            create_task: Request a background task. Keep the connection open until it finishes.
            **new: New identity fields, usually name, matching the model's master keys.

        Returns:
            AsyncFMGResponse: Clone operation status, with task metadata when provided by FortiManager.

        Examples:
            Inside an open connection, clone an existing address to an unused name:

            ```python
            from pyfortinet.fmg_api.firewall import Address

            response = await fmg.clone(Address(name="example-server"), name="example-server-copy")
            ```
        """
        response = AsyncFMGResponse(fmg=self)
        if isinstance(request, dict):  # JSON input, low-level operation
            return await super().clone(request, create_task=create_task)
        elif isinstance(request, FMGObject):  # high-level operation
            if not request.master_keys:
                raise FMGMissingMasterKeyException(f"Need to specify a master key for {request}")
            # master_key = first(request.master_keys.values())  # assume one master_key, like `name`
            # master_value = getattr(request, master_key)
            request.fmg_scope = request.fmg_scope or self._settings.adom
            return await super().clone(
                {
                    "url": request.get_url(method="clone"),
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
