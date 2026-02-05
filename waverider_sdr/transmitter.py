"""
SDR Transmitter Module

Implements signal transmission functionality with regulatory compliance.
"""

import logging
import numpy as np
from typing import Optional
from .config import SDRConfig

logger = logging.getLogger(__name__)


class SDRTransmitter:
    """
    SDR Transmitter for sending radio signals.
    
    Includes built-in safety checks and regulatory compliance features.
    """
    
    def __init__(self, config: SDRConfig):
        """
        Initialize SDR transmitter.
        
        Args:
            config: SDRConfig instance with transmitter parameters
        """
        self.config = config
        self.is_open = False
        self.is_transmitting = False
        
        if not config.tx_enabled:
            logger.warning(
                "Transmitter created but TX is disabled in config. "
                "Set tx_enabled=True to enable transmission."
            )
        
        logger.info(f"Initialized transmitter: {config}")
    
    def open(self) -> bool:
        """
        Open the SDR device for transmitting.
        
        Returns:
            True if successful, False otherwise
        """
        if self.is_open:
            logger.warning("Transmitter already open")
            return True
        
        if not self.config.tx_enabled:
            logger.error("Cannot open transmitter: TX is disabled in config")
            return False
        
        # Validate frequency before opening
        if not self._validate_frequency():
            return False
        
        try:
            logger.warning("="*70)
            logger.warning("OPENING TRANSMITTER")
            logger.warning("="*70)
            logger.warning("You are responsible for ensuring legal compliance!")
            logger.warning(f"Device: {self.config.device_id}")
            logger.warning(f"Frequency: {self.config.center_frequency/1e6:.3f} MHz")
            logger.warning(f"Sample rate: {self.config.sample_rate/1e6:.3f} MHz")
            logger.warning(f"TX gain: {self.config.tx_gain:.1f} dB")
            logger.warning(f"Max power: {self.config.max_tx_power:.3f} W")
            logger.warning("="*70)
            
            # In a real implementation, this would open the SDR hardware
            # For this example, we simulate successful opening
            self.is_open = True
            
            logger.info("Transmitter opened successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to open transmitter: {e}")
            return False
    
    def close(self):
        """Close the SDR device."""
        if not self.is_open:
            return
        
        if self.is_transmitting:
            self.stop_transmitting()
        
        logger.info("Closing transmitter")
        self.is_open = False
    
    def _validate_frequency(self) -> bool:
        """
        Validate the transmission frequency.
        
        Returns:
            True if frequency is valid, False otherwise
        """
        if not self.config.validate_tx_frequency(self.config.center_frequency):
            logger.error(
                f"Frequency {self.config.center_frequency/1e6:.3f} MHz is not "
                f"in allowed transmission bands"
            )
            logger.error("Allowed bands:")
            for min_freq, max_freq in self.config.allowed_tx_bands:
                logger.error(
                    f"  {min_freq/1e6:.3f} - {max_freq/1e6:.3f} MHz"
                )
            return False
        
        return True
    
    def _normalize_samples(self, samples: np.ndarray) -> np.ndarray:
        """
        Normalize samples to prevent overdrive.
        
        Args:
            samples: Complex samples to normalize
            
        Returns:
            Normalized samples
        """
        max_val = np.max(np.abs(samples))
        if max_val > 0:
            normalized = samples / max_val
            if max_val > 1.0:
                logger.warning(
                    f"Input samples were overdriven (max={max_val:.2f}), "
                    f"normalized to prevent distortion"
                )
            return normalized
        return samples
    
    def transmit_samples(self, samples: np.ndarray) -> bool:
        """
        Transmit IQ samples.
        
        Args:
            samples: NumPy array of complex samples to transmit
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_open:
            logger.error("Cannot transmit: device not open")
            return False
        
        if samples is None or len(samples) == 0:
            logger.error("Cannot transmit: no samples provided")
            return False
        
        # Normalize samples to prevent overdrive
        normalized_samples = self._normalize_samples(samples)
        
        # In a real implementation, this would send samples to SDR hardware
        logger.info(f"Transmitting {len(normalized_samples)} samples")
        logger.info(
            f"Sample power: {10*np.log10(np.mean(np.abs(normalized_samples)**2)):.2f} dB"
        )
        
        return True
    
    def start_transmitting(self) -> bool:
        """
        Start continuous transmission mode.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_open:
            logger.error("Cannot start transmitting: device not open")
            return False
        
        if self.is_transmitting:
            logger.warning("Already transmitting")
            return True
        
        logger.warning("Starting transmission")
        self.is_transmitting = True
        return True
    
    def stop_transmitting(self):
        """Stop continuous transmission."""
        if not self.is_transmitting:
            return
        
        logger.info("Stopping transmission")
        self.is_transmitting = False
    
    def generate_tone(
        self,
        frequency_offset: float = 0,
        duration: float = 0.1,
        amplitude: float = 0.5
    ) -> np.ndarray:
        """
        Generate a tone signal for testing.
        
        Args:
            frequency_offset: Frequency offset from center in Hz
            duration: Duration in seconds
            amplitude: Amplitude (0.0 to 1.0)
            
        Returns:
            NumPy array of complex samples
        """
        num_samples = int(duration * self.config.sample_rate)
        t = np.arange(num_samples) / self.config.sample_rate
        
        signal = amplitude * np.exp(2j * np.pi * frequency_offset * t)
        
        return signal.astype(np.complex64)
    
    def set_frequency(self, frequency: float) -> bool:
        """
        Set the center frequency.
        
        Args:
            frequency: Center frequency in Hz
            
        Returns:
            True if successful, False otherwise
        """
        if self.is_transmitting:
            logger.error("Cannot change frequency while transmitting")
            return False
        
        if frequency <= 0:
            logger.error("Invalid frequency")
            return False
        
        # Update config
        old_freq = self.config.center_frequency
        self.config.center_frequency = frequency
        
        # Validate new frequency
        if not self._validate_frequency():
            # Revert on failure
            self.config.center_frequency = old_freq
            return False
        
        logger.info(f"Set frequency to {frequency/1e6:.3f} MHz")
        return True
    
    def set_gain(self, gain: float) -> bool:
        """
        Set the transmitter gain.
        
        Args:
            gain: Gain in dB
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_open:
            logger.error("Cannot set gain: device not open")
            return False
        
        if gain < 0:
            logger.error("Gain cannot be negative")
            return False
        
        logger.info(f"Setting TX gain to {gain:.1f} dB")
        self.config.tx_gain = gain
        return True
    
    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
