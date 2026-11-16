"""Workspace context manager regression tests without a FortiManager."""

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest

from pyfortinet import AsyncFMG


@pytest.mark.parametrize("already_locked, keep_locked", [(False, False), (False, True), (True, False)])
@pytest.mark.parametrize("fail", [False, True])
def test_lock_context(client, already_locked, keep_locked, fail):
    """Release only locks acquired by this context, including on exceptions."""
    lock = client.lock
    lock._uses_workspace = True
    if already_locked:
        lock._locked_adoms.add("root")
    mock_type = AsyncMock if isinstance(client, AsyncFMG) else Mock
    lock.check_mode = mock_type()
    lock.lock_adoms = mock_type()
    lock.unlock_adoms = mock_type()

    def body(adom):
        assert adom == "root"
        if fail:
            raise RuntimeError("operation failed")

    async def use_async_context():
        async with client.lock_adom(keep_locked=keep_locked) as adom:
            body(adom)

    def use_context():
        if isinstance(client, AsyncFMG):
            asyncio.run(use_async_context())
        else:
            with client.lock_adom(keep_locked=keep_locked) as adom:
                body(adom)

    if fail:
        with pytest.raises(RuntimeError, match="operation failed"):
            use_context()
    else:
        use_context()
    assert lock.lock_adoms.call_count == int(not already_locked)
    assert lock.unlock_adoms.call_count == int(not already_locked and not keep_locked)
