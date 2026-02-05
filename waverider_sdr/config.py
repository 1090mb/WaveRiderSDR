"""
Configuration management for WaveRiderSDR.

Handles device settings, frequency ranges, and regulatory compliance.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SDRConfig:
    """Configuration class for SDR operations."""
    
    # Device settings
    device_id: str = "default"
    sample_rate: float = 2.4e6  # 2.4 MHz default
    
    # Frequency settings
    center_frequency: float = 100e6  # 100 MHz default
    bandwidth: float = 2e6  # 2 MHz default
    
    # Gain settings
    rx_gain: float = 20.0  # dB
    tx_gain: float = 10.0  # dB
    
    # Transmitter specific
    tx_enabled: bool = False
    max_tx_power: float = 1.0  # Watts
    
    # Regulatory
    require_license_check: bool = True
    allowed_tx_bands: Optional[list] = None
    
    def __post_init__(self):
        """Initialize default allowed transmit bands."""
        if self.allowed_tx_bands is None:
            # Default ISM bands (Industrial, Scientific and Medical)
            # These are example frequencies - users must comply with local regulations
            self.allowed_tx_bands = [
                (13.553e6, 13.567e6),    # 13.56 MHz ISM
                (26.957e6, 27.283e6),    # 27 MHz ISM
                (433.05e6, 434.79e6),    # 433 MHz ISM (ITU Region 1)
                (902e6, 928e6),          # 900 MHz ISM (ITU Region 2)
                (2.4e9, 2.5e9),          # 2.4 GHz ISM
                (5.725e9, 5.875e9),      # 5.8 GHz ISM
            ]
    
    def is_frequency_allowed_for_tx(self, frequency: float) -> bool:
        """
        Check if a frequency is allowed for transmission.
        
        Args:
            frequency: Frequency in Hz
            
        Returns:
            True if frequency is within allowed bands
        """
        if not self.tx_enabled:
            return False
            
        for band_start, band_end in self.allowed_tx_bands:
            if band_start <= frequency <= band_end:
                return True
        return False
    
    def validate(self) -> list:
        """
        Validate configuration parameters.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if self.sample_rate <= 0:
            errors.append("Sample rate must be positive")
        
        if self.center_frequency <= 0:
            errors.append("Center frequency must be positive")
        
        if self.bandwidth <= 0 or self.bandwidth > self.sample_rate:
            errors.append("Bandwidth must be positive and <= sample rate")
        
        if self.tx_enabled and self.require_license_check:
            if not self.is_frequency_allowed_for_tx(self.center_frequency):
                errors.append(
                    f"Frequency {self.center_frequency/1e6:.2f} MHz not in allowed TX bands. "
                    "Ensure you have proper authorization to transmit on this frequency."
                )
        
        if self.tx_gain < 0 or self.tx_gain > 100:
            errors.append("TX gain must be between 0 and 100 dB")
        
        if self.max_tx_power <= 0:
            errors.append("Max TX power must be positive")
        
        return errors
