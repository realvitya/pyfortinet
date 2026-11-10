"""Failure-path checks for the live-test cleanup infrastructure, without a device."""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from tests.lab.resources import AsyncLabResources, LabCleanupError, LabResources


@pytest.mark.parametrize("asynchronous", [False, True])
def test_partial_write_is_removed_and_already_deleted_objects_are_safe(asynchronous):
    mock = AsyncMock if asynchronous else Mock
    absent = SimpleNamespace(success=True, data=[{"data": []}])
    present = SimpleNamespace(success=True, data=[{"data": {"name": "owned"}}])
    client = SimpleNamespace(
        raise_on_error=False,
        get=mock(side_effect=[absent, present, absent]),
        delete=mock(return_value=SimpleNamespace(success=True)),
    )
    resources = AsyncLabResources(client) if asynchronous else LabResources(client)

    async def run():
        await resources.reserve("/owned")
        # Simulate a write that reached the server before the test failed.
        await resources.cleanup()
        await resources.cleanup()

    if asynchronous:
        asyncio.run(run())
    else:
        resources.reserve("/owned")
        resources.cleanup()
        resources.cleanup()
    client.delete.assert_called_once_with({"url": "/owned"})
    assert client.raise_on_error is False


@pytest.mark.parametrize("asynchronous", [False, True])
def test_existing_resource_is_never_registered_or_deleted(asynchronous):
    mock = AsyncMock if asynchronous else Mock
    client = SimpleNamespace(
        raise_on_error=True,
        get=mock(return_value=SimpleNamespace(success=True, data=[{"data": {"name": "existing"}}])),
        delete=mock(),
    )
    resources = AsyncLabResources(client) if asynchronous else LabResources(client)

    async def run():
        with pytest.raises(AssertionError, match="Refusing to reuse"):
            await resources.reserve("/existing")
        await resources.cleanup()

    if asynchronous:
        asyncio.run(run())
    else:
        with pytest.raises(AssertionError, match="Refusing to reuse"):
            resources.reserve("/existing")
        resources.cleanup()
    client.delete.assert_not_called()


@pytest.mark.parametrize("asynchronous", [False, True])
def test_cleanup_continues_in_reverse_order_and_reports_failures(asynchronous):
    calls = []
    client = SimpleNamespace(raise_on_error=False)
    resources = AsyncLabResources(client) if asynchronous else LabResources(client)

    def action(label):
        calls.append(label)
        assert client.raise_on_error
        if label == "zone":
            raise RuntimeError("sensitive diagnostic must not appear")

    async def async_action(label):
        action(label)

    for label in ["interface", "zone", "address"]:
        resources.defer(label, lambda label=label: async_action(label) if asynchronous else action(label))
    with pytest.raises(LabCleanupError, match=r"zone \(RuntimeError\)") as error:
        if asynchronous:
            asyncio.run(resources.cleanup())
        else:
            resources.cleanup()
    assert "sensitive" not in str(error.value)
    assert calls == ["address", "zone", "interface"]
    assert client.raise_on_error is False
