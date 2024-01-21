"""Fortinet Python library"""
__version__ = "0.0.1"
from pyfortinet.async_fmg import AsyncFMGBase
from pyfortinet.fmgbase import FMGBase, FMGResponse
from pyfortinet.fmg import FMG
from pyfortinet.settings import FMGSettings

__all__ = ("FMGBase", "FMG", "FMGResponse", "AsyncFMGBase", "FMGSettings")
