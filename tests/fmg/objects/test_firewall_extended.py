"""Independent live firewall scenarios; owned resources are cleaned before logout."""

import pytest

from pyfortinet.exceptions import FMGUnhandledException
from pyfortinet.fmg_api.firewall import InternetService
from tests.firewall_lab_cases import (
    GROUP_CASES,
    MAPPING_CASES,
    OBJECT_CASES,
    GroupCase,
    MappingCase,
    ObjectCase,
    assert_fields,
    assert_mapping,
    require_test_adom,
)


@pytest.mark.filterwarnings("ignore:Unverified")
class TestFirewallObjects:
    @pytest.mark.parametrize("case", OBJECT_CASES)
    def test_object_lifecycle(self, fmg, lab, case: ObjectCase):
        require_test_adom(fmg.adom)
        obj = lab.object(case.model, "obj", **case.fields)
        assert obj.add()
        loaded = (fmg.get(case.model(name=obj.name))).first()
        assert_fields(loaded, case.fields)
        assert loaded.name == obj.name

        setattr(obj, case.comment_field, "updated by isolated lab test")
        assert obj.update()
        obj.refresh()
        assert getattr(obj, case.comment_field) == "updated by isolated lab test"

        setattr(obj, case.comment_field, "set by isolated lab test")
        assert obj.set()
        loaded = (fmg.get(case.model(name=obj.name))).first()
        assert getattr(loaded, case.comment_field) == "set by isolated lab test"
        assert obj.delete()
        assert (fmg.get(case.model(name=obj.name))).first() is None

    @pytest.mark.parametrize("case", GROUP_CASES)
    def test_group_lifecycle(self, fmg, lab, case: GroupCase):
        require_test_adom(fmg.adom)
        first = lab.object(case.member_model, "first", **case.member_fields[0])
        second = lab.object(case.member_model, "second", **case.member_fields[1])
        assert first.add()
        assert second.add()
        group = lab.object(case.model, "group", member=[first, second], **case.group_fields)
        clone = lab.object(case.model, "clone")
        assert group.add()
        loaded = (fmg.get(case.model(name=group.name))).first()
        assert set(loaded.member) == {first.name, second.name}

        if case.clone_error:
            with pytest.raises(FMGUnhandledException, match=case.clone_error):
                group.clone(name=clone.name)
        else:
            assert group.clone(name=clone.name)
            cloned = (fmg.get(case.model(name=clone.name))).first()
            assert set(cloned.member) == {first.name, second.name}
            assert clone.delete()
        assert (fmg.get(case.model(name=clone.name))).first() is None

        group.member = [first.name]
        setattr(group, case.comment_field, "updated group")
        assert group.update()
        group.refresh()
        assert group.member == [first.name]
        assert getattr(group, case.comment_field) == "updated group"
        replacement = fmg.get_obj(case.model, name=group.name, member=[second], **case.group_fields)
        assert replacement.set()
        loaded = (fmg.get(case.model(name=group.name))).first()
        assert loaded.member == [second.name]
        assert group.delete()
        assert (fmg.get(case.model(name=group.name))).first() is None

    @pytest.mark.parametrize("case", MAPPING_CASES)
    def test_dynamic_mapping_lifecycle(self, fmg, lab, lab_device, case: MappingCase):
        require_test_adom(fmg.adom)
        scope = lab_device.get_vdom_scope("root")
        assert scope is not None and scope.name == "FG01" and scope.vdom == "root"
        obj = lab.object(case.parent.model, "mapped", **case.parent.fields)
        assert obj.add()
        obj.dynamic_mapping = [case.mapping_model(mapping__scope=scope, **case.overrides)]
        assert obj.update()
        obj.refresh()
        assert_mapping(obj, case, case.overrides)

        changed = {**case.overrides, case.field: case.changed_value}
        obj.dynamic_mapping = [case.mapping_model(mapping__scope=scope, **changed)]
        assert obj.update()
        obj.refresh()
        assert_mapping(obj, case, changed)

        obj.dynamic_mapping = []
        assert obj.update()
        obj.refresh()
        assert not obj.dynamic_mapping
        assert_fields(obj, case.parent.fields)
        assert obj.delete()
        assert (fmg.get(case.parent.model(name=obj.name))).first() is None

    def test_internet_service_lookup(self, fmg):
        require_test_adom(fmg.adom)
        catalog = fmg.get(
            {
                "url": f"/pm/config/adom/{fmg.adom}/obj/firewall/internet-service",
                "fields": ["id", "name"],
                "range": [0, 1],
            }
        )
        assert catalog.success
        rows = catalog.data[0].get("data")
        if not rows:
            pytest.skip("Lab Internet Service Database is empty; populate it before running this lookup")
        item = rows[0] if isinstance(rows, list) else rows
        assert item.get("id") is not None
        selected = fmg.get(InternetService(id=item["id"]))
        assert selected.success
        assert len(selected.data) == 1
        assert selected.first().id == item["id"]
        assert selected.first().name == item.get("name")
