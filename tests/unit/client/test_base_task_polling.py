"""Base clients can wait for tasks without the high-level object client."""

from unittest.mock import AsyncMock, Mock

import pytest
from pydantic import SecretStr

from pyfortinet import FMG, AsyncFMG, AsyncFMGBase, FMGBase
from tests.unit.conftest import resolve


@pytest.mark.parametrize("client_type", [FMGBase, AsyncFMGBase, FMG, AsyncFMG])
@pytest.mark.parametrize("as_list", [False, True])
def test_base_client_task_polling(client_type, as_list, monkeypatch):
    client = client_type(base_url="https://example.invalid", username="test", password="test")
    client._token = SecretStr("test-session")
    task = {"adom": 0, "end_tm": 0, "flags": 0, "id": 12, "line": [], "percent": 100, "state": "done"}
    mock_type = AsyncMock if issubclass(client_type, AsyncFMGBase) else Mock
    post = mock_type(return_value={"data": [task] if as_list else task, "status": {"code": 0}})
    monkeypatch.setattr(client, "_post", post)
    callback = Mock()
    assert resolve(client.wait_for_task(12, callback=callback)) == "done"
    callback.assert_called_once_with(100, "")
    params = post.call_args.kwargs["request"]["params"][0]
    assert params["url"] == "/task/task"
    assert params["filter"] == ["id", "==", 12]
