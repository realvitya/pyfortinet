# Advanced usage / extension of the handler

It is possible to extend the FMG handler capabilities with custom methods. If the existing methods are not enough or
seem too atomic, custom methods and behaviour can be attached to the handler.

Here is an example why and how it can be done:

## Adding human-readable actions

Let's say we want to add more complex tasks as method to the handler itself so our code can be clean and focused on its
task.

```python title="mypkg/mymodule/myfmg.py"
from pyfortinet import FMG
from pyfortinet.fmg_api.dvmdb import Device
from pyfortinet.fmg_api.dvmcmd import DeviceTask
from pyfortinet.fmg_api.policy import PolicyPackage, PackageSettings, Policy


class MyFMG(FMG):
    """Extra actions for FortiManager"""
    def create_firewall(self, name: str, address: str, serial: str) -> bool:
        """This method creates a device along with a default firewall policy

        Firewall will be deleted if existed before!

        Notes:
            This method may leave garbage after itself if exception is raised anywhere!

        Arguments:
            name (str): The name of the device
            address (str): The IP address of the device
            serial (str): The serial number of the device

        Returns:
            (bool): True if the device was created successfully, False otherwise
        """
        # sanity check
        name = name.strip().upper()
        try:
            # create device
            device: Device = Device(name=name, sn=serial, os_ver="7.0", mr=2, ip=address)
            if existing_device:=self.get(device).first():
                delete_job = DeviceTask(adom=self.adom, device=existing_device, action="del")
                self.exec(delete_job)
            job = DeviceTask(adom=self.adom, device=device)
            result = self.exec(job)
            status = result.wait_for_task()
            if status != "done":
                return False
            fw: Device = self.get(Device(name=name)).first()
            # create PolicyPackage
            pp_settings = PackageSettings(fwpolicy_implicit_log="enable")
            pp = self.get_obj(PolicyPackage, name=name, scope_member=[fw.get_vdom_scope("root")], package_settings=pp_settings)
            pp.add()
            pp.refresh()
            default_policies = [
                Policy(pkg=pp.name, name="Default explicit deny 1->2", srcaddr=["all"], dstaddr=["all"], srcintf=["port1"],
                       dstintf=["port2"], action="deny", service=["ALL"], logtraffic="disable", schedule=["always"]),
                Policy(pkg=pp.name, name="Default explicit deny 2->1", srcaddr=["all"], dstaddr=["all"], srcintf=["port2"],
                       dstintf=["port1"], action="deny", service=["ALL"], logtraffic="disable", schedule=["always"])
            ]
            self.add(default_policies)
            return True
        except Exception:
            return False
```

Then your code is cleaner by simply calling the modified handler with custom method:

```python title="mypkg/mymodule/app.py"
from mymodule.myfmg import MyFMG
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

conn_data = {
    "base_url": "https://fmg",
    "verify": False,
    "username": "admin",
    "password": "verysecret",
    "adom": "root"
}

with MyFMG(**conn_data) as fmg:
    fmg.create_firewall("mytestfw", "1.1.1.1", "FG100FTK22345678")
```
