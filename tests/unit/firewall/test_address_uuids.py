"""Optional UUIDs validate consistently with optimized Python."""

import subprocess
import sys

import pytest
from pydantic import ValidationError

from pyfortinet.fmg_api.firewall import Address, AddressGroup


@pytest.mark.parametrize("model", [Address, AddressGroup])
def test_optional_address_uuid(model):
    assert model(uuid=None).uuid is None
    with pytest.raises(ValidationError):
        model(uuid="invalid")
    value = "12345678123456781234567812345678"
    assert model(uuid=value).uuid == "12345678-1234-5678-1234-567812345678"


def test_optimized_python_still_validates_address_uuids():
    script = """
from pydantic import ValidationError
from pyfortinet.fmg_api.firewall import Address, AddressGroup
for model in (Address, AddressGroup):
    if model(uuid=None).uuid is not None:
        raise RuntimeError('Optional UUID was changed')
    try:
        model(uuid='invalid')
    except ValidationError:
        pass
    else:
        raise RuntimeError('Invalid UUID accepted')
"""
    subprocess.run([sys.executable, "-O", "-c", script], check=True, capture_output=True, text=True)
