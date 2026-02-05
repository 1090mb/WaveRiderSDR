"""
WaveRiderSDR - Software Defined Radio Library with Bidirectional Capability

This package provides tools for working with Software Defined Radio (SDR) hardware,
including both receiving and transmitting radio signals.
"""

from .config import SDRConfig
from .receiver import SDRReceiver
from .transmitter import SDRTransmitter

__version__ = "1.0.0"
__all__ = ["SDRConfig", "SDRReceiver", "SDRTransmitter"]
