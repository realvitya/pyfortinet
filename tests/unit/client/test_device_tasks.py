"""Device task construction and operation-specific inputs."""

import pytest
from pydantic import ValidationError

from pyfortinet.fmg_api.dvmcmd import DeviceCommand, DeviceTask
from pyfortinet.fmg_api.dvmdb import Device


@pytest.mark.parametrize("device", ["FGT1", Device(name="FGT1"), DeviceCommand(name="FGT1")])
def test_delete_task_accepts_names_and_models(device):
    task = DeviceTask(action="del", adom="root", device=device)
    assert task.model_dump(by_alias=True)["device"] == "FGT1"
    assert task.get_url() == "/dvm/cmd/del/device"


@pytest.mark.parametrize("device", [42, {}, None])
def test_invalid_device_raises_validation_error(device):
    with pytest.raises(ValidationError):
        DeviceTask(action="del", adom="root", device=device)


def test_add_task_requires_device_configuration():
    with pytest.raises(ValidationError, match="Adding a device requires"):
        DeviceTask(action="add", adom="root", device="FGT1")
    task = DeviceTask(action="add", adom="root", device=DeviceCommand(name="FGT1"))
    assert task.model_dump(by_alias=True)["device"]["name"] == "FGT1"
