"""Shared request preparation for the synchronous and asynchronous clients."""

import re
from inspect import isclass

from pyfortinet.exceptions import FMGWrongRequestException
from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.common import F, text_to_filter


def prepare_batch(request, *, allow_objects=False):
    """Normalize a write request and reject empty or mixed batches."""
    requests = request if isinstance(request, list) else [request]
    if not requests:
        raise FMGWrongRequestException("Request list must not be empty")
    if isinstance(requests[0], dict):
        expected_type = dict
    elif allow_objects and isinstance(requests[0], FMGObject):
        expected_type = FMGObject
    else:
        raise FMGWrongRequestException(f"Wrong type of request received: {request}")
    if not all(isinstance(item, expected_type) for item in requests):
        raise FMGWrongRequestException("Batch requests must all be dictionaries or all be FMGObject instances")
    return requests


def prepare_get(request, adom, *, filters=None, scope=None, fields=None, loadsub=True, options=None):  # noqa: PLR0913
    """Build high-level GET parameters and retain the effective object scope."""
    if isinstance(filters, str):
        filters = text_to_filter(filters)
    object_scope = scope or adom
    if isinstance(request, FMGObject):
        request.fmg_scope = request.fmg_scope or object_scope
        url = request.get_url()
        object_scope = getattr(request, "adom", None) or request.fmg_scope
        for field in request.model_dump_for_filter():
            value = getattr(request, field.replace(" ", "_").replace("-", "_"))
            condition = F(**{field: value})
            filters = filters & condition if filters else condition
    elif isclass(request) and issubclass(request, FMGObject):
        url = re.sub(r"/{(?!scope).*?}", "", request._url.default)
        if object_scope != "global" and not object_scope.startswith("adom/"):
            object_scope = f"adom/{object_scope}"
        url = url.replace("{scope}", object_scope)
    else:
        raise FMGWrongRequestException(f"Wrong type of request received: {request}")

    parameters = {"url": url, "loadsub": 1 if loadsub else 0}
    if filters:
        parameters["filter"] = filters.generate()
    if fields is not None:
        parameters["fields"] = fields
    if options:
        parameters["option"] = options
    return parameters, object_scope


def prepare_refresh(obj):
    """Preserve scope and URL parameters while looking up an object's identity."""
    fields = {
        name: getattr(obj, name)
        for name, definition in type(obj).model_fields.items()
        if name in obj.master_keys.values() or (definition.exclude and getattr(obj, name) is not None)
    }
    return type(obj)(**fields, fmg_scope=obj.fmg_scope)


def response_url_fields(request):
    """Carry URL-only parent parameters omitted by configuration GET replies."""
    if not isinstance(request, FMGObject):
        return {}
    return {
        name: getattr(request, name)
        for name, definition in type(request).model_fields.items()
        if definition.exclude
        and f"{{{name}}}" in request._url
        and not request._url.endswith(f"/{{{name}}}")
        and getattr(request, name) is not None
    }
