"""
WaveRiderSDR - A Software Defined Radio with full bidirectional capability.

This package provides both receiving and transmitting functionality for SDR operations.
"""

__version__ = "0.1.0"
__author__ = "1090mb"

from .receiver import SDRReceiver
from .transmitter import SDRTransmitter
from .config import SDRConfig

__all__ = ["SDRReceiver", "SDRTransmitter", "SDRConfig"]
