#!/usr/bin/env python3
"""
Example: Signal transmission with WaveRiderSDR

This example demonstrates how to use the SDR transmitter to send radio signals.

WARNING: Transmitting radio signals requires proper licensing and authorization.
Only run this example if you have the necessary permissions and are in compliance
with all applicable radio regulations.
"""

import sys
import logging
import numpy as np
from waverider_sdr import SDRTransmitter, SDRConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Demonstrate basic transmitting functionality."""
    
    logger.info("=== WaveRiderSDR Transmitter Example ===")
    logger.warning(
        "\n" + "="*70 + "\n"
        "REGULATORY WARNING\n"
        "="*70 + "\n"
        "Transmitting radio signals without proper authorization is illegal\n"
        "in most jurisdictions. Ensure you:\n"
        "  1. Have the appropriate amateur radio or commercial license\n"
        "  2. Are transmitting on authorized frequencies\n"
        "  3. Comply with power limits and technical standards\n"
        "  4. Follow all local telecommunications regulations\n"
        "="*70 + "\n"
    )
    
    # Create configuration with TX enabled
    config = SDRConfig(
        device_id="default",
        center_frequency=433.92e6,  # 433.92 MHz (ISM band in some regions)
        sample_rate=2.4e6,          # 2.4 MHz
        tx_gain=20.0,               # 20 dB gain
        tx_enabled=True,            # Enable transmission
        max_tx_power=0.1,           # 100 mW (low power for safety)
        require_license_check=True,
    )
    
    logger.info(f"Frequency: {config.center_frequency/1e6:.3f} MHz")
    logger.info(f"Sample Rate: {config.sample_rate/1e6:.2f} MHz")
    logger.info(f"TX Power: {config.max_tx_power} W")
    
    # Prompt for user confirmation
    try:
        response = input("\nDo you have authorization to transmit on this frequency? (yes/no): ")
        if response.lower() != "yes":
            logger.info("Transmission cancelled by user")
            return 0
    except (EOFError, KeyboardInterrupt):
        logger.info("\nTransmission cancelled")
        return 0
    
    # Create transmitter
    transmitter = SDRTransmitter(config)
    
    # Open the device
    if not transmitter.open():
        logger.error("Failed to open transmitter")
        return 1
    
    try:
        # Generate a test tone
        logger.info("Generating test tone...")
        tone = transmitter.generate_tone(
            frequency_offset=10e3,  # 10 kHz offset from center
            duration=0.1,           # 100 ms
            amplitude=0.5           # 50% amplitude
        )
        
        logger.info(f"Generated {len(tone)} samples")
        
        # Transmit the tone
        logger.info("Transmitting tone...")
        if transmitter.transmit_samples(tone):
            logger.info("Transmission successful!")
        else:
            logger.error("Transmission failed")
            return 1
        
        # Demonstrate frequency tuning
        logger.info("Changing frequency to 434.0 MHz...")
        if transmitter.set_frequency(434.0e6):
            # Generate and transmit another tone
            tone2 = transmitter.generate_tone(
                frequency_offset=0,
                duration=0.1,
                amplitude=0.3
            )
            transmitter.transmit_samples(tone2)
            logger.info("Second transmission complete!")
        
    finally:
        # Clean up
        transmitter.close()
        logger.info("Transmitter closed")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
