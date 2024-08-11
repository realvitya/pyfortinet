"""Device Manager Command"""

from typing import Literal, Union, List, Optional

from pydantic import Field, model_validator, field_validator, AliasChoices

from pyfortinet.fmg_api import FMGExecObject, FMGObject
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.dvmdb import Device, DEVICE_ACTION

FLAGS = Literal["none", "create_task", "nonblocking", "log_dev"]


class DeviceCommand(Device):
    """Device extended with data suitable for task handling

    Attributes:
        name (str): object name
        adm_usr (str): admin user
        adm_pass (list[str]): admin password
        app_ver (str): App DB version
        av_ver (str): Anti-Virus DB version
        checksum (str): Configuration checksum
        conf_status (CONF_STATUS): Configuration status
        desc (str): Device description
        device_action (DEVICE_ACTION): Device add or remove action
        device_blueprint (str): Device blueprint name
        ha_group_id (int): HA group ID
        ha_group_name (str): HA group Name
        hostname (str): hostname
        ip (str): Device IP address
        meta_fields (dict): Meta fields data
        mgmt_if (str): management interface name
        mgmt_mode (MGMT_MODE): Management mode of the device
        mgmt_uuid (str):
        mgt_vdom (str): management VDOM
        mr (int): OS minor version
        os_type (OS_TYPE): OS type of the device
        os_ver (OS_VER): OS major version
        patch (int): OS patch version
        psk (str): pre-shared secret
        sn (str): Serial number of the device
        version (int):
        platform_str (str): platform name (device model)
        vdom (list[VDOM]): VDOM list
        ha_slave: Optional[List[HASlave]]
    """

    device_action: Optional[DEVICE_ACTION] = Field(
        "",
        description="Leave empty for real device!",
        validation_alias=AliasChoices("device action", "device_action"),
        serialization_alias="device action",
    )
    device_blueprint: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("device blueprint", "device_blueprint"),
        serialization_alias="device blueprint",
    )
    platform_str: Optional[str] = None


class DeviceTask(FMGExecObject):
    """Add/Del device request

    Attributes:
        action (Literal["add","del"]): Add or Del device
        adom: ADOM to use
        device (Union[str, DeviceAction, ModelDevice]): Device to add/del
        flags (List[FLAGS]): Job flags
        groups (List[Scope]): device groups
    """

    # internal attributes
    _url = "/dvm/cmd/{action}/device"
    _params = {}
    action: Literal["add", "del"] = Field("add", exclude=True, validate_default=True)
    # api attributes
    adom: str
    device: Union[Device, DeviceCommand]
    flags: list[FLAGS] = ["create_task", "non-blocking"]
    groups: Optional[list[Scope]] = None

    @field_validator("device", mode="before")
    def ensure_device_type(cls, device):
        if isinstance(device, DeviceCommand):
            return device
        elif isinstance(device, Device):
            device = DeviceCommand(**device.model_dump(by_alias=True))
            return device
        raise TypeError("Device must be of type Device or DeviceCommand!")

    @model_validator(mode="after")
    def validate_devicejob(self) -> "DeviceTask":
        """Validate device job"""
        self._url = self._url.replace("{action}", self.action)
        if self.action == "del":
            self.device = self.device.name  # deleting a device requires device id or name
        return self
