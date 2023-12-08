"""Fortinet Python library"""
__version__ = "0.0.1"
from pyfortinet.async_fmg import AsyncFMG
from pyfortinet.fmg import FMG
from pyfortinet.settings import FMGSettings

__all__ = ("FMG", "AsyncFMG", "FMGSettings")
