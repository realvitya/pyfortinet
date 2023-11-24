"""Async FMG connection"""
import functools
import logging
from typing import Any, Optional

import aiohttp
from pydantic import SecretStr

from pyfortinet.fmg_api.exceptions import FMGException, FMGTokenException
from pyfortinet.fmg_api.settings import FMGSettings

logger = logging.getLogger(__name__)


def auth_required(func):
    """Decorator to provide authentication for the method

    Args:
        func: function to handle authentication errors

    Returns:
        function with authentication handling enabled
    """

    @functools.wraps(func)
    async def decorated(self, *args, **kwargs):
        """method which needs authentication"""
        if not self._token:
            raise FMGTokenException("No token was obtained. Open connection first!")
        try:
            return await func(self, *args, **kwargs)
        except FMGException as err:
            try:  # try again after refreshing token
                self._token = self._get_token()  # pylint: disable=protected-access  # decorator of methods
                return await func(self, *args, **kwargs)
            except FMGException as err2:
                raise err2 from err

    return decorated


class AsyncFMG:
    """Fortimanager connection class"""

    def __init__(self, settings: FMGSettings):
        logger.debug("Initializing connection to %s", settings.base_url)
        self._settings = settings
        self._token: Optional[SecretStr] = None
        self._session: Optional[aiohttp.ClientSession] = None

    async def open(self):
        """open connection"""
        self._session = aiohttp.ClientSession()
        self._token = self._get_token()

    async def close(self):
        """close connection"""
        # Logout and expire token
        request = {
            "id": 1,
            "method": "exec",
            "params": [{"url": "/sys/logout"}],
            "session": self._token.get_secret_value(),
        }
        try:
            async with await self._session.post(
                self._settings.base_url, json=request, verify=self._settings.verify
            ) as req:
                status = (await req.json()).get("result", [{}])[0].get("status", {})
            if status.get("code") != 0:
                logger.warning("Logout failed!")
        except Exception:
            logger.warning("Logout failed!")

        await self._session.close()
        logger.debug("Closed session")

    async def __enter__(self):
        self.open()
        return self

    async def __exit__(self, exc_type, exc_value, exc_tb):
        await self.close()

    async def _post(self, request: dict) -> Any:
        async with self._session.post(self._settings.base_url, json=request, verify=self._settings.verify) as req:
            results = (await req.json()).get("result", [])
        if any(status := result["status"] for result in results if result["status"]["code"] != 0):
            raise FMGException(status)
        return results[0] if len(results) == 1 else results

    async def _get_token(self) -> SecretStr:
        """Get authentication token

        Raises:

        """
        logger.debug("Getting token..")
        request = {
            "id": 1,
            "method": "exec",
            "params": [
                {
                    "data": {"passwd": self._settings.password.get_secret_value(), "user": self._settings.username},
                    "url": "/sys/login/user",
                }
            ],
        }
        try:
            async with self._session.post(self._settings.base_url, json=request, verify=self._settings.verify) as req:
                status = (await req.json()).get("result", [{}])[0].get("status", {})
                if status.get("code") != 0:
                    raise FMGTokenException("Login failed, wrong credentials!")
                token = (await req.json()).get("session", "")
                logger.debug("Token obtained")
        except FMGTokenException as err:
            logger.error("Can't gather token: %s", err)
            raise err
        except Exception as err:
            logger.error("Can't gather token: %s", err)
            raise err
        return SecretStr(token)

    @auth_required
    def get_version(self) -> str:
        """Gather FMG version"""
        request = {
            "method": "get",
            "params": [{"url": "/sys/status"}],
            "id": 1,
            "session": self._token.get_secret_value(),
        }
        req = self._post(request)
        return req["data"]["Version"]
