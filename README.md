# WaveRiderSDR

The only SDR with full features and rolling updates.

## Features

### 1. Bidirectional SDR Operation
- **Receive Signals**: Capture incoming IQ data streams for analysis
- **Transmit Signals**: Send radio signals with proper regulatory safeguards
- **Regulatory Compliance**: Built-in frequency validation and power limiting
- **ISM Band Support**: Pre-configured for common ISM bands
- **Safety Features**: TX disabled by default, frequency whitelist enforcement

### 2. Frequency Band Selection and Visualization
- **Band Selection**: Choose from HF, VHF, UHF, and SHF frequency ranges
- **Interactive Band Plan**: Visual display of frequency allocations
- **Zoom and Pan**: Detailed exploration of specific frequency ranges
- **Color-Coded Allocations**: Easy identification of Amateur, Broadcasting, Mobile, Satellite, and Government services
- **Current Frequency Marker**: Real-time indication of tuned frequency

### 3. Recording and Playback
- **Record IQ Streams**: Capture incoming IQ data streams for offline analysis
- **HDF5 Storage**: Efficient storage format with metadata support
- **Playback Capability**: Review previously recorded data seamlessly
- **Recording Controls**: Easy-to-use interface for starting, stopping, and managing recordings

### 4. Configurable Workspaces
- **Customizable Layouts**: Organize the application interface to match your workflow
- **Save/Load Workspaces**: Store multiple workspace configurations
- **Auto-save**: Automatically save workspace on exit
- **Quick Switching**: Easily switch between different workspace layouts

### 5. Customizable User Interface
- **Multiple Themes**: Choose from Dark, Light, and High Contrast themes
- **Font Scaling**: Adjust text size from 0.5x to 2.0x for better readability
- **Accessible Design**: High-contrast mode and scalable fonts for accessibility
- **Dockable Panels**: Rearrange panels to suit your preferences

### 6. Device Compatibility Database
- **Pre-configured Devices**: Database of known SDR devices with optimal settings
- **Device Information**: Frequency ranges, sample rates, gain settings, and features
- **Search Functionality**: Quickly find devices by name, manufacturer, or type
- **Supported Devices**:
  - RTL-SDR dongles
  - HackRF One
  - Airspy Mini/R2
  - SDRplay RSP1A
  - bladeRF x40
  - And more...

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install from source

```bash
git clone https://github.com/1090mb/WaveRiderSDR.git
cd WaveRiderSDR
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

## Usage

### Using the Band Plan Visualizer

The WaveRiderSDR includes a web-based frequency band plan visualizer:

1. Open `index.html` in a modern web browser
2. Use the **Band Selector** dropdown to choose:
   - **HF (3-30 MHz)**: Shortwave radio, amateur radio, international broadcasting
   - **VHF (30-300 MHz)**: FM radio, TV broadcasting, amateur radio, aviation
   - **UHF (300-3000 MHz)**: TV broadcasting, mobile phones, GPS, WiFi, Bluetooth
   - **SHF (3-30 GHz)**: Satellite communications, radar, 5G, WiFi 6
3. Enter frequencies directly or use tuning buttons (±10MHz, ±1MHz, ±100kHz)
4. **Interact with the band plan**:
   - Hover over allocations to see names
   - Click on allocations for detailed information
   - Use Zoom In/Out buttons to explore specific ranges
   - Current frequency shown with red marker

### Using the SDR Library (Receive/Transmit)

#### Receiving Signals

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
receiver.start_receiving()

# Read samples
samples = receiver.read_samples(10000)

# Get signal strength
rssi = receiver.get_signal_strength()
print(f"Signal strength: {rssi:.2f} dBm")

# Clean up
receiver.close()
```

#### Transmitting Signals

⚠️ **WARNING**: Transmitting radio signals requires proper licensing and authorization in most jurisdictions.

```python
from waverider_sdr import SDRTransmitter, SDRConfig

# Configure transmitter (TX must be explicitly enabled)
config = SDRConfig(
    center_frequency=433.92e6,  # 433.92 MHz (ISM band)
    sample_rate=2.4e6,
    tx_gain=20.0,
    tx_enabled=True,           # Enable transmission
    max_tx_power=0.1           # 100 mW
)

# Create and open transmitter
transmitter = SDRTransmitter(config)
if transmitter.open():
    # Generate a test tone
    tone = transmitter.generate_tone(
        frequency_offset=10e3,  # 10 kHz offset
        duration=0.1            # 100 ms
    )
    
    # Transmit
    transmitter.transmit_samples(tone)
    transmitter.close()
```

#### Running Examples

The `examples/` directory contains demonstration scripts:

```bash
# Receive-only example
python examples/receive_example.py

# Transmit-only example (requires authorization)
python examples/transmit_example.py

# Bidirectional operation
python examples/bidirectional_example.py
```

### Running the Application

```bash
python -m waverider.main
```

Or if installed:

```bash
waverider
```

### Recording IQ Data

1. Click the "Start Recording" button in the Recording panel
2. Recording will begin with default settings (2.048 MHz sample rate, 100 MHz center frequency)
3. Click "Stop Recording" to finish
4. Recordings are saved in the `recordings/` directory as HDF5 files

### Playing Back Recordings

1. Click "Load" in the Playback section
2. Select a recording file (.h5)
3. Use Play/Pause/Stop controls to navigate the recording
4. Progress bar shows current position

### Managing Workspaces

1. Go to **Workspace** → **Manage Workspaces**
2. Select a workspace to load, or create a new one
3. Workspace configurations include:
   - Window size and position
   - Panel visibility and arrangement
   - Toolbar settings

### Customizing the Theme

1. Go to **View** → **Theme Settings**
2. Choose from available themes:
   - **Dark**: Easy on the eyes with blue accents
   - **Light**: Professional light appearance
   - **High Contrast**: Enhanced visibility for accessibility
3. Adjust font scale for better readability
4. Click Apply or OK to save changes

### Browsing Device Database

1. Open the Devices panel (View → Devices)
2. Browse the list of supported SDR devices
3. Use the search box to find specific devices
4. Filter by device type
5. Click on a device to see detailed specifications

## Regulatory Compliance and Safety

### Important Legal Notice

**Transmitting radio signals is regulated by law in most countries.** Before transmitting, you must:

1. **Obtain Proper Authorization**: You may need an amateur radio license, commercial license, or other authorization
2. **Use Authorized Frequencies**: Only transmit on frequencies you are legally permitted to use
3. **Respect Power Limits**: Comply with maximum power output regulations
4. **Follow Technical Standards**: Adhere to modulation, bandwidth, and emission standards
5. **Know Your Regulations**: Familiarize yourself with:
   - FCC regulations (USA)
   - ETSI standards (Europe)
   - Local telecommunications laws

### Built-in Safety Features

The WaveRiderSDR transmitter includes safety features to prevent accidental violations:

- **TX Disabled by Default**: Transmission must be explicitly enabled in configuration
- **Frequency Validation**: Checks against allowed ISM bands before transmitting
- **Power Limiting**: Sample normalization to prevent overdrive
- **Configuration Validation**: Pre-transmission checks for valid parameters
- **Comprehensive Logging**: All operations logged with regulatory warnings

### Default Allowed Frequency Bands

By default, the transmitter restricts operation to common ISM bands:

- 13.56 MHz ISM
- 27 MHz ISM  
- 433 MHz ISM (ITU Region 1)
- 900 MHz ISM (ITU Region 2)
- 2.4 GHz ISM
- 5.8 GHz ISM

**Note**: Even within ISM bands, specific regulations apply. Users are solely responsible for compliance with all applicable laws.

### Disclaimer

This software is provided for educational and research purposes. **Users are solely responsible for ensuring their use of this software complies with all applicable laws and regulations.** The authors and contributors assume no liability for misuse or any damages resulting from the use of this software.

## Project Structure

```
WaveRiderSDR/
├── waverider/
│   ├── core/              # Core functionality
│   │   ├── recorder.py    # IQ recording
│   │   ├── player.py      # IQ playback
│   │   └── workspace.py   # Workspace management
│   ├── ui/                # User interface
│   │   ├── main_window.py
│   │   ├── recording_panel.py
│   │   ├── device_panel.py
│   │   ├── workspace_dialog.py
│   │   └── theme_dialog.py
│   ├── config/            # Configuration
│   │   └── theme.py       # Theme management
│   ├── database/          # Device database
│   │   └── devices.py
│   └── main.py           # Application entry point
├── waverider_sdr/         # SDR library (RX/TX)
│   ├── config.py          # Configuration with validation
│   ├── receiver.py        # Signal receiving
│   ├── transmitter.py     # Signal transmission with safeguards
│   └── __init__.py
├── examples/              # Example scripts
│   ├── receive_example.py
│   ├── transmit_example.py
│   └── bidirectional_example.py
├── index.html            # Band plan visualizer
├── app.js                # Visualization logic
├── styles.css            # Web interface styling
├── recordings/           # Recorded IQ data (created on first run)
├── workspaces/           # Workspace configurations
├── config/               # User configuration files
├── requirements.txt      # Python dependencies
├── setup.py             # Installation script
└── README.md            # This file
```

## File Formats

### Recording Files (.h5)
Recordings are stored in HDF5 format with the following structure:
- **iq_data**: Complex64 dataset containing IQ samples
- **Attributes**: Metadata including sample rate, center frequency, timestamps

### Workspace Files (.yaml)
Workspace configurations are stored in YAML format with:
- Window geometry
- Panel visibility and positions
- Toolbar settings
- User preferences

### Device Database (devices.json)
JSON format containing device specifications:
- Device identification
- Frequency ranges
- Sample rates
- Gain settings
- Feature flags

## Development

### Adding New Devices

Edit `waverider/database/devices.py` and add device specifications to the `DEFAULT_DEVICES` list.

### Creating Custom Themes

Edit `waverider/config/theme.py` and add new theme definitions to the `THEMES` dictionary.

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests. 
