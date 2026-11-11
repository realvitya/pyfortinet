"""The firewall package preserves its historical public import paths."""

import importlib
import pickle

import pytest

from pyfortinet.fmg_api import firewall

PUBLIC_MODELS = [
    ("address", "Address"),
    ("address", "AddressGroup"),
    ("address", "AddressTagging"),
    ("service", "PortRange"),
    ("service", "ServiceCategory"),
    ("service", "ServiceCustom"),
    ("service", "ServiceGroup"),
    ("profile_group", "ProfileGroup"),
    ("proxy_address", "ProxyAddress"),
    ("proxy_address", "ProxyAddressHeaderGroup"),
    ("proxy_address", "ProxyAddressTagging"),
    ("proxy_address_group", "ProxyAddressGroup"),
    ("proxy_address_group", "ProxyAddressGroupTagging"),
    ("internet_service", "InternetService"),
    ("vip", "VIP"),
    ("vip", "VIPDynamicMapping"),
    ("ip_pool", "IPPool"),
    ("ip_pool", "IPPoolDynamicMapping"),
    ("ip_pool_group", "IPPoolGroup"),
]

PUBLIC_TYPES = [
    ("types", "ADDRESS_GROUP_CATEGORY"),
    ("types", "ADDRESS_GROUP_TYPE"),
    ("types", "ADDRESS_TYPE"),
    ("types", "APP_SERVICE_TYPE"),
    ("types", "CHECK_RESET_RANGE"),
    ("types", "CLEARPASS_SPT"),
    ("types", "DIRTY"),
    ("types", "ENABLE_DISABLE"),
    ("types", "HELPER"),
    ("types", "OBJ_TYPE"),
    ("types", "PROTOCOL"),
    ("types", "SDN_ADDR_TYPE"),
    ("types", "SUB_TYPE"),
    ("service", "PORT_RANGE_TYPE"),
]


@pytest.mark.parametrize("module, name", PUBLIC_MODELS)
def test_public_models_are_reexported_from_their_submodules(module, name):
    implementation = importlib.import_module("pyfortinet.fmg_api.firewall." + module)
    assert getattr(firewall, name) is getattr(implementation, name)
    assert name in firewall.__all__


@pytest.mark.parametrize("module, name", PUBLIC_TYPES)
def test_historical_type_imports_resolve_to_the_defining_alias(module, name):
    implementation = importlib.import_module("pyfortinet.fmg_api.firewall." + module)
    assert getattr(firewall, name) is getattr(implementation, name)
    assert name not in firewall.__all__


@pytest.mark.parametrize("name", ["Address", "AddressGroup", "PortRange", "ServiceCustom", "ProfileGroup"])
def test_historical_pickle_class_paths_still_resolve(name):
    # Protocol-0 GLOBAL references use the same class lookup as pickles created before the move.
    historical_reference = ("cpyfortinet.fmg_api.firewall\n" + name + "\n.").encode("ascii")
    assert pickle.loads(historical_reference) is getattr(firewall, name)


def test_package_exports_only_classes_and_port_ranges_still_normalize():
    assert all(isinstance(getattr(firewall, name), type) for name in firewall.__all__)
    service = firewall.ServiceCustom(tcp_portrange=firewall.PortRange(destination_end="443"))
    assert service.model_dump(by_alias=True, exclude_none=True) == {"tcp-portrange": ["443"]}


@pytest.mark.parametrize("associated_interface", ["port1", ["port1"]])
def test_address_list_field_does_not_shadow_generic_annotations(associated_interface):
    address = firewall.Address(
        associated_interface=associated_interface,
        list=[{"ip": "192.0.2.1"}],
        macaddr=["00:11:22:33:44:55"],
    )
    assert isinstance(address.list[0], firewall.Address.AddressList)
    assert address.model_dump(by_alias=True, exclude_none=True) == {
        "associated-interface": "port1",
        "list": [{"ip": "192.0.2.1"}],
        "macaddr": ["00:11:22:33:44:55"],
    }
