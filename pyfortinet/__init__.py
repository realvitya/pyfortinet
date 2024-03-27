"""Fortinet Python library"""

__version__ = "0.0.1.post1"

from pyfortinet.fmg_api.async_fmgbase import AsyncFMGBase, AsyncFMGResponse
from pyfortinet.fmg_api.fmg import FMG
from pyfortinet.fmg_api.async_fmg import AsyncFMG
from pyfortinet.fmg_api.fmgbase import FMGBase, FMGResponse
from pyfortinet.settings import FMGSettings

__all__ = ("FMGBase", "FMG", "FMGResponse", "AsyncFMGBase", "AsyncFMG", "AsyncFMGResponse", "FMGSettings")
