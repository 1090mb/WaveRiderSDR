"""
SDR Receiver Module

Implements signal receiving functionality for SDR devices.
"""

import logging
import numpy as np
from typing import Optional
from .config import SDRConfig

logger = logging.getLogger(__name__)


class SDRReceiver:
    """
    SDR Receiver for capturing radio signals.
    
    Provides functionality to receive IQ samples from SDR hardware.
    """
    
    def __init__(self, config: SDRConfig):
        """
        Initialize SDR receiver.
        
        Args:
            config: SDRConfig instance with receiver parameters
        """
        self.config = config
        self.is_open = False
        self.is_receiving = False
        self._last_samples = None
        
        logger.info(f"Initialized receiver: {config}")
    
    def open(self) -> bool:
        """
        Open the SDR device for receiving.
        
        Returns:
            True if successful, False otherwise
        """
        if self.is_open:
            logger.warning("Receiver already open")
            return True
        
        try:
            logger.info(f"Opening receiver on device: {self.config.device_id}")
            logger.info(f"Center frequency: {self.config.center_frequency/1e6:.3f} MHz")
            logger.info(f"Sample rate: {self.config.sample_rate/1e6:.3f} MHz")
            logger.info(f"RX gain: {self.config.rx_gain:.1f} dB")
            
            # In a real implementation, this would open the SDR hardware
            # For this example, we simulate successful opening
            self.is_open = True
            
            logger.info("Receiver opened successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to open receiver: {e}")
            return False
    
    def close(self):
        """Close the SDR device."""
        if not self.is_open:
            return
        
        if self.is_receiving:
            self.stop_receiving()
        
        logger.info("Closing receiver")
        self.is_open = False
    
    def start_receiving(self) -> bool:
        """
        Start receiving samples.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_open:
            logger.error("Cannot start receiving: device not open")
            return False
        
        if self.is_receiving:
            logger.warning("Already receiving")
            return True
        
        logger.info("Starting reception")
        self.is_receiving = True
        return True
    
    def stop_receiving(self):
        """Stop receiving samples."""
        if not self.is_receiving:
            return
        
        logger.info("Stopping reception")
        self.is_receiving = False
    
    def read_samples(self, num_samples: int = 1024) -> Optional[np.ndarray]:
        """
        Read IQ samples from the receiver.
        
        Args:
            num_samples: Number of complex samples to read
            
        Returns:
            NumPy array of complex64 samples, or None if error
        """
        if not self.is_open:
            logger.error("Cannot read samples: device not open")
            return None
        
        if not self.is_receiving:
            logger.error("Cannot read samples: not receiving")
            return None
        
        # In a real implementation, this would read from SDR hardware
        # For this example, we generate simulated samples
        # Simulate a noisy signal with some tone components
        t = np.arange(num_samples) / self.config.sample_rate
        
        # Add some simulated signals
        signal = (
            0.1 * np.exp(2j * np.pi * 10e3 * t) +  # 10 kHz tone
            0.05 * np.exp(2j * np.pi * -15e3 * t) +  # -15 kHz tone
            0.02 * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))  # noise
        )
        
        self._last_samples = signal.astype(np.complex64)
        return self._last_samples
    
    def set_frequency(self, frequency: float) -> bool:
        """
        Set the center frequency.
        
        Args:
            frequency: Center frequency in Hz
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_open:
            logger.error("Cannot set frequency: device not open")
            return False
        
        if frequency <= 0:
            logger.error("Invalid frequency")
            return False
        
        logger.info(f"Setting frequency to {frequency/1e6:.3f} MHz")
        self.config.center_frequency = frequency
        return True
    
    def set_gain(self, gain: float) -> bool:
        """
        Set the receiver gain.
        
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
        
        logger.info(f"Setting RX gain to {gain:.1f} dB")
        self.config.rx_gain = gain
        return True
    
    def get_signal_strength(self) -> float:
        """
        Get the received signal strength indicator (RSSI).
        
        Returns:
            Signal strength in dBm
        """
        if self._last_samples is None or len(self._last_samples) == 0:
            return -100.0  # Very weak signal
        
        # Calculate power in dBm
        power = np.mean(np.abs(self._last_samples) ** 2)
        if power > 0:
            rssi = 10 * np.log10(power) + 30  # Convert to dBm (arbitrary reference)
        else:
            rssi = -100.0
        
        return rssi
    
    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
