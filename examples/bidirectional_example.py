#!/usr/bin/env python3
"""
Example: Bidirectional SDR operation

This example demonstrates using both receiver and transmitter together,
showcasing the full bidirectional capability of WaveRiderSDR.
"""

import sys
import logging
import time
from waverider_sdr import SDRReceiver, SDRTransmitter, SDRConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Demonstrate bidirectional SDR operation."""
    
    logger.info("=== WaveRiderSDR Bidirectional Example ===")
    
    # Configuration for receiving
    rx_config = SDRConfig(
        device_id="rx_device",
        center_frequency=433.92e6,  # 433.92 MHz
        sample_rate=2.4e6,
        rx_gain=30.0,
    )
    
    # Configuration for transmitting
    tx_config = SDRConfig(
        device_id="tx_device", 
        center_frequency=433.92e6,  # Same frequency
        sample_rate=2.4e6,
        tx_gain=15.0,
        tx_enabled=True,
        max_tx_power=0.1,  # 100 mW
    )
    
    # Create receiver and transmitter
    receiver = SDRReceiver(rx_config)
    transmitter = SDRTransmitter(tx_config)
    
    # Open both devices
    logger.info("Opening receiver...")
    if not receiver.open():
        logger.error("Failed to open receiver")
        return 1
    
    logger.info("Opening transmitter...")
    if not transmitter.open():
        logger.error("Failed to open transmitter")
        receiver.close()
        return 1
    
    try:
        # Start receiving
        logger.info("Starting receiver...")
        receiver.start_receiving()
        
        # Measure background noise
        logger.info("Measuring background signal level...")
        background_rssi = receiver.get_signal_strength()
        logger.info(f"Background RSSI: {background_rssi:.2f} dBm")
        
        # Generate and transmit a test signal
        logger.info("Generating test signal...")
        test_signal = transmitter.generate_tone(
            frequency_offset=0,  # At center frequency
            duration=0.5         # 500 ms
        )
        
        logger.info("Transmitting test signal...")
        transmitter.transmit_samples(test_signal)
        
        # Brief pause to simulate propagation
        time.sleep(0.1)
        
        # Measure signal during transmission
        logger.info("Measuring signal level during transmission...")
        tx_rssi = receiver.get_signal_strength()
        logger.info(f"Signal RSSI during TX: {tx_rssi:.2f} dBm")
        
        # Calculate signal increase
        signal_increase = tx_rssi - background_rssi
        logger.info(f"Signal increase: {signal_increase:.2f} dB")
        
        logger.info("\n=== Bidirectional Operation Summary ===")
        logger.info(f"RX Frequency: {rx_config.center_frequency/1e6:.3f} MHz")
        logger.info(f"TX Frequency: {tx_config.center_frequency/1e6:.3f} MHz")
        logger.info(f"Background: {background_rssi:.2f} dBm")
        logger.info(f"With Signal: {tx_rssi:.2f} dBm")
        logger.info("Bidirectional capability demonstrated successfully!")
        
    finally:
        # Clean up
        logger.info("Cleaning up...")
        receiver.stop_receiving()
        receiver.close()
        transmitter.close()
        logger.info("All devices closed")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
