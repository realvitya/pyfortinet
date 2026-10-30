"""Verify native read timeouts against a local HTTP peer that never responds."""

import asyncio
import socket
import threading

import aiohttp
import pytest
import requests
from pydantic import SecretStr

from pyfortinet import AsyncFMGBase, FMGBase


@pytest.fixture
def unresponsive_http_peer():
    stop = threading.Event()
    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    listener.listen()
    listener.settimeout(2)

    def accept_request():
        try:
            connection, _ = listener.accept()
        except (OSError, TimeoutError):
            return
        with connection:
            stop.wait(2)

    thread = threading.Thread(target=accept_request, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{listener.getsockname()[1]}"
    finally:
        stop.set()
        listener.close()
        thread.join(timeout=3)
        assert not thread.is_alive()


def test_sync_native_read_timeout(unresponsive_http_peer):
    client = FMGBase(base_url=unresponsive_http_peer, username="test", password="test", timeout=0.05, retry_attempts=1)
    client._token = SecretStr("test-session")
    with requests.Session() as session:
        client._session = session
        with pytest.raises(requests.Timeout):
            client.get({"url": "/sys/status"})


def test_async_native_read_timeout(unresponsive_http_peer):
    async def run():
        client = AsyncFMGBase(
            base_url=unresponsive_http_peer, username="test", password="test", timeout=0.05, retry_attempts=1
        )
        client._token = SecretStr("test-session")
        async with aiohttp.ClientSession() as session:
            client._session = session
            with pytest.raises(asyncio.TimeoutError):
                await client.get({"url": "/sys/status"})

    asyncio.run(run())
