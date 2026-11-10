"""Input normalization shared by the schema-backed firewall objects."""

from typing import Optional
from uuid import UUID

from pyfortinet.fmg_api import FMGObject


def as_list(value: object) -> Optional[list[object]]:
    """Accept one value or the API's array form, preserving absent values."""
    if value is None or isinstance(value, list):
        return value
    return [value]


def reference_names(value: object) -> Optional[list[str]]:
    """Turn named high-level object references into the API's name arrays."""
    values = as_list(value)
    if values is None:
        return None
    result = []
    for item in values:
        name = getattr(item, "name", None) if isinstance(item, FMGObject) else item
        if not isinstance(name, str) or not name:
            raise ValueError("References must be nonempty names or objects with a name")
        result.append(name)
    return result


def uuid_string(value: Optional[str]) -> Optional[str]:
    """Validate UUID values while leaving omitted attributes unset."""
    return str(UUID(value)) if value is not None else None
