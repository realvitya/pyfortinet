"""Workspace operation results and local lock bookkeeping."""

from unittest.mock import AsyncMock, Mock

import pytest

from pyfortinet import AsyncFMG, AsyncFMGResponse, FMGResponse
from pyfortinet.exceptions import FMGException, FMGLockException

from .conftest import resolve


@pytest.fixture
def execute(client, monkeypatch):
    asynchronous = isinstance(client, AsyncFMG)
    response_type = AsyncFMGResponse if asynchronous else FMGResponse
    result = response_type(data=[{"status": {"code": 0}}], success=True, fmg=client)
    mock_type = AsyncMock if asynchronous else Mock
    execute = mock_type(return_value=result)
    monkeypatch.setattr(client, "exec", execute)
    return execute


def test_unlock_subset_retains_other_locks(client, execute):
    client.lock.locked_adoms.update(["first", "other"])
    resolve(client.lock.unlock_adoms("first"))
    assert client.lock.locked_adoms == {"other"}
    assert execute.call_args.kwargs["request"]["url"] == "/dvmdb/adom/first/workspace/unlock/"


def test_unlock_success_without_local_lock(client, execute):
    resolve(client.lock.unlock_adoms("first"))
    assert not client.lock.locked_adoms


def test_unlock_failure_keeps_failed_lock(client, execute):
    client.lock.locked_adoms.update(["first", "other"])
    execute.return_value = FMGResponse(data=[{"error": "unlock failed"}], success=False)
    with pytest.raises(FMGException, match="first"):
        resolve(client.lock.unlock_adoms("first"))
    assert client.lock.locked_adoms == {"first", "other"}


@pytest.mark.parametrize("method", ["lock_adoms", "unlock_adoms"])
def test_workspace_results_include_all_operations(client, execute, method):
    result = resolve(getattr(client.lock, method)("first", "other"))
    assert result.success
    assert result.fmg is client
    assert [next(iter(item)) for item in result.data] == ["first", "other"]
    assert all(item[adom].success for item, adom in zip(result.data, ["first", "other"]))


def test_unsuccessful_lock_does_not_mark_adom_locked(client, execute):
    execute.return_value = FMGResponse(data=[{"status": {"code": -1}}], success=False)
    with pytest.raises(FMGLockException):
        resolve(client.lock.lock_adoms("first"))
    assert not client.lock.locked_adoms


def test_unsuccessful_unlock_without_local_lock_is_reported(client, execute):
    execute.return_value = FMGResponse(data=[], success=False)
    with pytest.raises(FMGException, match="first"):
        resolve(client.lock.unlock_adoms("first"))
