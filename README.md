# WaveRiderSDR
The only SDR with full features and rolling updates.

## Overview

WaveRiderSDR is a Software Defined Radio (SDR) library providing **full bidirectional capability** - both receiving and transmitting radio signals. This project enables users to work with radio frequencies in compliance with proper regulations and standards.

## Features

- **Bidirectional Operation**: Both receive (RX) and transmit (TX) capabilities
- **Regulatory Compliance**: Built-in safety checks and frequency band restrictions
- **Flexible Configuration**: Configurable sample rates, gains, and frequencies
- **Signal Processing**: Support for IQ sample processing and signal generation
- **Multiple SDR Devices**: Support for various SDR hardware platforms

## Installation

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

## Quick Start

### Receiving Signals

```python
from waverider_sdr import SDRReceiver, SDRConfig

# Configure receiver
config = SDRConfig(
    center_frequency=100e6,  # 100 MHz
    sample_rate=2.4e6,       # 2.4 MHz
    rx_gain=30.0             # 30 dB
)

# Create and open receiver
receiver = SDRReceiver(config)
receiver.open()

# Start receiving
receiver.start_receiving()
samples = receiver.read_samples(num_samples=10000)

# Clean up
receiver.close()
```

### Transmitting Signals

⚠️ **WARNING**: Transmitting radio signals requires proper licensing and authorization in most jurisdictions.

```python
from waverider_sdr import SDRTransmitter, SDRConfig

# Configure transmitter
config = SDRConfig(
    center_frequency=433.92e6,  # 433.92 MHz (ISM band)
    sample_rate=2.4e6,
    tx_gain=20.0,
    tx_enabled=True,           # Must explicitly enable TX
    max_tx_power=0.1           # 100 mW
)

# Create and open transmitter
transmitter = SDRTransmitter(config)
if transmitter.open():
    # Generate and transmit a tone
    tone = transmitter.generate_tone(
        frequency_offset=10e3,  # 10 kHz offset
        duration=0.1            # 100 ms
    )
    transmitter.transmit_samples(tone)
    transmitter.close()
```

## Examples

The `examples/` directory contains demonstration scripts:

- `receive_example.py` - Basic signal receiving
- `transmit_example.py` - Signal transmission with regulatory warnings
- `bidirectional_example.py` - Combined RX/TX operation

Run examples:

```bash
python examples/receive_example.py
python examples/transmit_example.py
python examples/bidirectional_example.py
```

## Regulatory Compliance

### Important Legal Notice

Transmitting radio signals is regulated by law in most countries. Before transmitting:

1. **Obtain Proper Authorization**: You may need an amateur radio license, commercial license, or other authorization
2. **Use Authorized Frequencies**: Only transmit on frequencies you are legally permitted to use
3. **Respect Power Limits**: Comply with maximum power output regulations
4. **Follow Technical Standards**: Adhere to modulation, bandwidth, and emission standards
5. **Know Your Regulations**: Familiarize yourself with:
   - FCC regulations (USA)
   - ETSI standards (Europe)
   - Local telecommunications laws

### Default Safety Features

WaveRiderSDR includes built-in safety features:

- Transmission is **disabled by default** (`tx_enabled=False`)
- Frequency validation against allowed ISM bands
- Power limiting and sample normalization
- Configuration validation before transmission
- Comprehensive logging and warnings

### Allowed Frequency Bands

By default, the transmitter restricts operation to common ISM (Industrial, Scientific, Medical) bands:

- 13.56 MHz ISM
- 27 MHz ISM  
- 433 MHz ISM (ITU Region 1)
- 900 MHz ISM (ITU Region 2)
- 2.4 GHz ISM
- 5.8 GHz ISM

**Note**: Even within ISM bands, specific regulations apply. Users are responsible for compliance with all applicable laws.

## Configuration

The `SDRConfig` class manages all device settings:

```python
config = SDRConfig(
    device_id="default",              # Device identifier
    sample_rate=2.4e6,                # Sample rate (Hz)
    center_frequency=100e6,           # Center frequency (Hz)
    bandwidth=2e6,                    # Bandwidth (Hz)
    rx_gain=20.0,                     # RX gain (dB)
    tx_gain=10.0,                     # TX gain (dB)
    tx_enabled=False,                 # Enable/disable TX
    max_tx_power=1.0,                 # Max TX power (W)
    require_license_check=True,       # Enforce frequency checks
    allowed_tx_bands=[...]            # Custom TX frequency bands
)
```

## Architecture

- `waverider_sdr/config.py` - Configuration management and validation
- `waverider_sdr/receiver.py` - SDR receiver implementation
- `waverider_sdr/transmitter.py` - SDR transmitter with safety checks
- `examples/` - Demonstration scripts

## Requirements

- Python 3.7+
- NumPy 1.20+

## License

MIT License - see LICENSE file for details

## Disclaimer

This software is provided for educational and research purposes. Users are solely responsible for ensuring their use of this software complies with all applicable laws and regulations. The authors and contributors assume no liability for misuse or any damages resulting from the use of this software.

## Contributing

Contributions are welcome! Please ensure any transmit-related features include appropriate safety checks and regulatory warnings. 
