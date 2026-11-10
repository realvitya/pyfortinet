"""Independent live firewall scenarios; owned resources are cleaned before logout."""

import pytest

from pyfortinet.exceptions import FMGUnhandledException
from pyfortinet.fmg_api.firewall import InternetService
from tests.conftest import AsyncTestCase
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


class TestFirewallObjects(AsyncTestCase):
    @pytest.mark.parametrize("case", OBJECT_CASES)
    async def test_object_lifecycle(self, fmg, lab, case: ObjectCase):
        require_test_adom(fmg.adom)
        obj = await lab.object(case.model, "obj", **case.fields)
        assert await obj.add()
        loaded = (await fmg.get(case.model(name=obj.name))).first()
        assert_fields(loaded, case.fields)
        assert loaded.name == obj.name

        setattr(obj, case.comment_field, "updated by isolated lab test")
        assert await obj.update()
        await obj.refresh()
        assert getattr(obj, case.comment_field) == "updated by isolated lab test"

        setattr(obj, case.comment_field, "set by isolated lab test")
        assert await obj.set()
        loaded = (await fmg.get(case.model(name=obj.name))).first()
        assert getattr(loaded, case.comment_field) == "set by isolated lab test"
        assert await obj.delete()
        assert (await fmg.get(case.model(name=obj.name))).first() is None

    @pytest.mark.parametrize("case", GROUP_CASES)
    async def test_group_lifecycle(self, fmg, lab, case: GroupCase):
        require_test_adom(fmg.adom)
        first = await lab.object(case.member_model, "first", **case.member_fields[0])
        second = await lab.object(case.member_model, "second", **case.member_fields[1])
        assert await first.add()
        assert await second.add()
        group = await lab.object(case.model, "group", member=[first, second], **case.group_fields)
        clone = await lab.object(case.model, "clone")
        assert await group.add()
        loaded = (await fmg.get(case.model(name=group.name))).first()
        assert set(loaded.member) == {first.name, second.name}

        if case.clone_error:
            with pytest.raises(FMGUnhandledException, match=case.clone_error):
                await group.clone(name=clone.name)
        else:
            assert await group.clone(name=clone.name)
            cloned = (await fmg.get(case.model(name=clone.name))).first()
            assert set(cloned.member) == {first.name, second.name}
            assert await clone.delete()
        assert (await fmg.get(case.model(name=clone.name))).first() is None

        group.member = [first.name]
        setattr(group, case.comment_field, "updated group")
        assert await group.update()
        await group.refresh()
        assert group.member == [first.name]
        assert getattr(group, case.comment_field) == "updated group"
        replacement = fmg.get_obj(case.model, name=group.name, member=[second], **case.group_fields)
        assert await replacement.set()
        loaded = (await fmg.get(case.model(name=group.name))).first()
        assert loaded.member == [second.name]
        assert await group.delete()
        assert (await fmg.get(case.model(name=group.name))).first() is None

    @pytest.mark.parametrize("case", MAPPING_CASES)
    async def test_dynamic_mapping_lifecycle(self, fmg, lab, lab_device, case: MappingCase):
        require_test_adom(fmg.adom)
        scope = lab_device.get_vdom_scope("root")
        assert scope is not None and scope.name == "FG01" and scope.vdom == "root"
        obj = await lab.object(case.parent.model, "mapped", **case.parent.fields)
        assert await obj.add()
        obj.dynamic_mapping = [case.mapping_model(mapping__scope=scope, **case.overrides)]
        assert await obj.update()
        await obj.refresh()
        assert_mapping(obj, case, case.overrides)

        changed = {**case.overrides, case.field: case.changed_value}
        obj.dynamic_mapping = [case.mapping_model(mapping__scope=scope, **changed)]
        assert await obj.update()
        await obj.refresh()
        assert_mapping(obj, case, changed)

        obj.dynamic_mapping = []
        assert await obj.update()
        await obj.refresh()
        assert not obj.dynamic_mapping
        assert_fields(obj, case.parent.fields)
        assert await obj.delete()
        assert (await fmg.get(case.parent.model(name=obj.name))).first() is None

    async def test_internet_service_lookup(self, fmg):
        require_test_adom(fmg.adom)
        catalog = await fmg.get(
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
        selected = await fmg.get(InternetService(id=item["id"]))
        assert selected.success
        assert len(selected.data) == 1
        assert selected.first().id == item["id"]
        assert selected.first().name == item.get("name")
