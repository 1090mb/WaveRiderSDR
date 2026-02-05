#!/usr/bin/env python3
"""
Example: Basic signal receiving with WaveRiderSDR

This example demonstrates how to use the SDR receiver to capture radio signals.
"""

import sys
import logging
from waverider_sdr import SDRReceiver, SDRConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Demonstrate basic receiving functionality."""
    
    # Create configuration
    config = SDRConfig(
        device_id="default",
        center_frequency=100e6,  # 100 MHz FM broadcast band
        sample_rate=2.4e6,       # 2.4 MHz
        rx_gain=30.0,            # 30 dB gain
    )
    
    logger.info("=== WaveRiderSDR Receiver Example ===")
    logger.info(f"Frequency: {config.center_frequency/1e6:.2f} MHz")
    logger.info(f"Sample Rate: {config.sample_rate/1e6:.2f} MHz")
    
    # Create receiver
    receiver = SDRReceiver(config)
    
    # Open the device
    if not receiver.open():
        logger.error("Failed to open receiver")
        return 1
    
    try:
        # Start receiving
        receiver.start_receiving()
        
        # Read some samples
        logger.info("Reading samples...")
        samples = receiver.read_samples(num_samples=10000)
        logger.info(f"Received {len(samples)} complex samples")
        
        # Get signal strength
        rssi = receiver.get_signal_strength()
        logger.info(f"Signal strength (RSSI): {rssi:.2f} dBm")
        
        # Demonstrate frequency tuning
        logger.info("Tuning to 101.5 MHz...")
        receiver.set_frequency(101.5e6)
        
        # Read more samples at new frequency
        samples = receiver.read_samples(num_samples=10000)
        rssi = receiver.get_signal_strength()
        logger.info(f"Signal strength at 101.5 MHz: {rssi:.2f} dBm")
        
        logger.info("Receiving complete!")
        
    finally:
        # Clean up
        receiver.stop_receiving()
        receiver.close()
        logger.info("Receiver closed")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
