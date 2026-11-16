"""Offline fixtures shared by synchronous and asynchronous client tests."""

import asyncio
import inspect
from unittest.mock import AsyncMock, Mock

import pytest
from pydantic import SecretStr

from pyfortinet import FMG, AsyncFMG


@pytest.fixture(params=[FMG, AsyncFMG], ids=["sync", "async"])
def client(request):
    """Create an authenticated client without opening a network connection."""
    instance = request.param(base_url="https://example.invalid", username="test", password="test", adom="root")
    instance._token = SecretStr("test-session")
    return instance


@pytest.fixture
def post(client, monkeypatch):
    """Replace the transport while preserving its calling convention."""
    mock = AsyncMock() if isinstance(client, AsyncFMG) else Mock()
    monkeypatch.setattr(client, "_post", mock)
    return mock


def resolve(value):
    """Run an async client operation or return a synchronous result."""
    return asyncio.run(value) if inspect.isawaitable(value) else value
