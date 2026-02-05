"""
SDR Configuration Module

Manages SDR device configuration with validation and safety checks.
"""

import logging
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)


class SDRConfig:
    """
    Configuration class for SDR devices.
    
    Manages parameters for both receive and transmit operations, with built-in
    validation and regulatory compliance checks.
    """
    
    # Common ISM (Industrial, Scientific, Medical) bands that are generally
    # available for unlicensed use in many jurisdictions
    DEFAULT_ALLOWED_TX_BANDS = [
        (13.553e6, 13.567e6),    # 13.56 MHz ISM
        (26.957e6, 27.283e6),    # 27 MHz ISM
        (433.05e6, 434.79e6),    # 433 MHz ISM (Region 1)
        (902.0e6, 928.0e6),      # 900 MHz ISM (Region 2)
        (2.4e9, 2.5e9),          # 2.4 GHz ISM
        (5.725e9, 5.875e9),      # 5.8 GHz ISM
    ]
    
    def __init__(
        self,
        device_id: str = "default",
        sample_rate: float = 2.4e6,
        center_frequency: float = 100e6,
        bandwidth: Optional[float] = None,
        rx_gain: float = 20.0,
        tx_gain: float = 0.0,
        tx_enabled: bool = False,
        max_tx_power: float = 1.0,
        require_license_check: bool = True,
        allowed_tx_bands: Optional[List[Tuple[float, float]]] = None
    ):
        """
        Initialize SDR configuration.
        
        Args:
            device_id: Device identifier
            sample_rate: Sample rate in Hz (default: 2.4 MHz)
            center_frequency: Center frequency in Hz (default: 100 MHz)
            bandwidth: Bandwidth in Hz (default: None, uses sample rate)
            rx_gain: Receive gain in dB (default: 20.0)
            tx_gain: Transmit gain in dB (default: 0.0)
            tx_enabled: Enable transmit functionality (default: False)
            max_tx_power: Maximum transmit power in watts (default: 1.0)
            require_license_check: Enforce frequency whitelist (default: True)
            allowed_tx_bands: List of (min_freq, max_freq) tuples for TX
        """
        self.device_id = device_id
        self.sample_rate = sample_rate
        self.center_frequency = center_frequency
        self.bandwidth = bandwidth if bandwidth is not None else sample_rate
        self.rx_gain = rx_gain
        self.tx_gain = tx_gain
        self.tx_enabled = tx_enabled
        self.max_tx_power = max_tx_power
        self.require_license_check = require_license_check
        
        if allowed_tx_bands is None:
            self.allowed_tx_bands = self.DEFAULT_ALLOWED_TX_BANDS.copy()
        else:
            self.allowed_tx_bands = allowed_tx_bands
        
        # Validate configuration
        self._validate()
    
    def _validate(self):
        """Validate configuration parameters."""
        if self.sample_rate <= 0:
            raise ValueError("Sample rate must be positive")
        
        if self.center_frequency <= 0:
            raise ValueError("Center frequency must be positive")
        
        if self.bandwidth <= 0:
            raise ValueError("Bandwidth must be positive")
        
        if self.rx_gain < 0:
            raise ValueError("RX gain cannot be negative")
        
        if self.tx_gain < 0:
            raise ValueError("TX gain cannot be negative")
        
        if self.max_tx_power <= 0:
            raise ValueError("Max TX power must be positive")
        
        if self.tx_enabled:
            logger.warning(
                "TRANSMIT MODE ENABLED - Ensure you have proper authorization "
                "and are operating within legal frequency bands"
            )
    
    def validate_tx_frequency(self, frequency: float) -> bool:
        """
        Validate if a frequency is allowed for transmission.
        
        Args:
            frequency: Frequency in Hz to validate
            
        Returns:
            True if frequency is allowed, False otherwise
        """
        if not self.require_license_check:
            logger.warning(
                "License check disabled - transmitting without validation"
            )
            return True
        
        # Check if frequency is within any allowed band
        for min_freq, max_freq in self.allowed_tx_bands:
            if min_freq <= frequency <= max_freq:
                return True
        
        return False
    
    def __repr__(self):
        return (
            f"SDRConfig(device_id='{self.device_id}', "
            f"sample_rate={self.sample_rate}, "
            f"center_frequency={self.center_frequency}, "
            f"tx_enabled={self.tx_enabled})"
        )
