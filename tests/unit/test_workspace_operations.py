"""Workspace operation results and local lock bookkeeping."""

from unittest.mock import AsyncMock, Mock, call

import pytest

from pyfortinet import AsyncFMG, AsyncFMGResponse, FMGResponse
from pyfortinet.exceptions import FMGException, FMGLockException

from .conftest import resolve

MODES = [
    (0, False),
    ("0", False),
    ("disabled", False),
    (1, True),
    ("1", True),
    ("normal", True),
    (2, True),
    ("2", True),
    ("workflow", True),
]


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


@pytest.mark.parametrize("mode, expected", [(0, False), ("0", False), ("disabled", False), (1, True), ("normal", True)])
def test_workspace_mode_discovery(client, monkeypatch, mode, expected):
    mock_type = AsyncMock if isinstance(client, AsyncFMG) else Mock
    response = FMGResponse(data=[{"data": {"workspace-mode": mode}}], success=True)
    monkeypatch.setattr(client, "get", mock_type(return_value=response))
    resolve(client.lock.check_mode())
    assert client.lock.uses_workspace is expected


@pytest.mark.parametrize(
    "data, success", [([{"error": "denied"}], False), ([], True), ([{"data": {}}], True), ([{"data": None}], True)]
)
def test_failed_workspace_discovery_does_not_cache_a_mode(client, monkeypatch, data, success):
    mock_type = AsyncMock if isinstance(client, AsyncFMG) else Mock
    response = FMGResponse(data=data, success=success)
    monkeypatch.setattr(client, "get", mock_type(return_value=response))
    with pytest.raises(FMGLockException, match="workspace mode"):
        resolve(client.lock.check_mode())
    assert client.lock.uses_workspace is None


@pytest.mark.parametrize("global_mode", [0, "0", "disabled", 1, "1", "normal", 2, "2", "workflow", 3, "3", "per-adom"])
@pytest.mark.parametrize("adom_mode, expected", MODES)
def test_global_and_adom_mode_combinations(client, monkeypatch, global_mode, adom_mode, expected):
    mock_type = AsyncMock if isinstance(client, AsyncFMG) else Mock
    global_response = FMGResponse(data=[{"data": {"workspace-mode": global_mode}}], success=True)
    adom_response = FMGResponse(data=[{"data": {"workspace_mode": adom_mode}}], success=True)
    get = mock_type(side_effect=[global_response, adom_response])
    monkeypatch.setattr(client, "get", get)
    resolve(client.lock.check_mode("other"))
    per_adom = global_mode in (3, "3", "per-adom")
    assert client.lock.uses_workspace is (expected if per_adom else global_mode not in (0, "0", "disabled"))
    assert get.call_count == (2 if per_adom else 1)
    if per_adom:
        assert get.call_args.args == ({"url": "/dvmdb/adom/other", "fields": ["workspace_mode"]},)


@pytest.mark.parametrize(
    "data, success",
    [
        ([], True),
        ([{"data": {}}], True),
        ([{"data": None}], True),
        ([{"data": {"workspace_mode": 99}}], True),
        ([], False),
    ],
)
def test_failed_adom_discovery_clears_previous_mode(client, monkeypatch, data, success):
    client.lock._uses_workspace = True
    mock_type = AsyncMock if isinstance(client, AsyncFMG) else Mock
    get = mock_type(
        side_effect=[
            FMGResponse(data=[{"data": {"workspace-mode": "per-adom"}}], success=True),
            FMGResponse(data=data, success=success),
        ]
    )
    monkeypatch.setattr(client, "get", get)
    with pytest.raises(FMGLockException, match="workspace mode"):
        resolve(client.lock.check_mode())
    assert client.lock.uses_workspace is None
    assert get.call_args.args[0]["url"] == "/dvmdb/adom/root"


def test_lock_call_filters_adoms_by_their_own_mode(client, execute, monkeypatch):
    mock_type = AsyncMock if isinstance(client, AsyncFMG) else Mock
    global_response = FMGResponse(data=[{"data": {"workspace-mode": "per-adom"}}], success=True)
    get = mock_type(
        side_effect=[
            global_response,
            FMGResponse(data=[{"data": {"workspace_mode": 1}}], success=True),
            global_response,
            FMGResponse(data=[{"data": {"workspace_mode": 0}}], success=True),
        ]
    )
    monkeypatch.setattr(client, "get", get)
    resolve(client.lock("first", "other"))
    assert client.lock.locked_adoms == {"first"}
    execute.assert_called_once_with(request={"url": "/dvmdb/adom/first/workspace/lock/"})


@pytest.mark.parametrize("adom", ["global", "Global"])
@pytest.mark.parametrize("global_mode, expected", [*MODES, (3, False), ("3", False), ("per-adom", False)])
def test_global_database_mode_discovery(client, monkeypatch, adom, global_mode, expected):
    mock_type = AsyncMock if isinstance(client, AsyncFMG) else Mock
    get = mock_type(return_value=FMGResponse(data=[{"data": {"workspace-mode": global_mode}}], success=True))
    monkeypatch.setattr(client, "get", get)
    resolve(client.lock.check_mode(adom))
    assert client.lock.uses_workspace is expected
    assert get.call_count == 1


def test_global_database_lock_skipped_in_per_adom_mode(client, execute, monkeypatch):
    mock_type = AsyncMock if isinstance(client, AsyncFMG) else Mock
    get = mock_type(return_value=FMGResponse(data=[{"data": {"workspace-mode": "per-adom"}}], success=True))
    monkeypatch.setattr(client, "get", get)
    resolve(client.lock("global"))
    execute.assert_not_called()
    assert not client.lock.locked_adoms


def test_explicit_context_discovers_each_target_mode(client, execute, monkeypatch):
    mock_type = AsyncMock if isinstance(client, AsyncFMG) else Mock
    global_response = FMGResponse(data=[{"data": {"workspace-mode": "per-adom"}}], success=True)
    get = mock_type(
        side_effect=[
            global_response,
            FMGResponse(data=[{"data": {"workspace_mode": 0}}], success=True),
            global_response,
            FMGResponse(data=[{"data": {"workspace_mode": 1}}], success=True),
        ]
    )
    monkeypatch.setattr(client, "get", get)

    async def use_async_contexts():
        async with client.lock_adom("other"):
            assert not client.lock.locked_adoms
        async with client.lock_adom("first"):
            assert client.lock.locked_adoms == {"first"}

    if isinstance(client, AsyncFMG):
        resolve(use_async_contexts())
    else:
        with client.lock_adom("other"):
            assert not client.lock.locked_adoms
        with client.lock_adom("first"):
            assert client.lock.locked_adoms == {"first"}
    assert not client.lock.locked_adoms
    assert execute.call_args_list == [
        call(request={"url": "/dvmdb/adom/first/workspace/lock/"}),
        call(request={"url": "/dvmdb/adom/first/workspace/unlock/"}),
    ]
