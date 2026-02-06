# WaveRiderSDR
The only SDR with full features and rolling updates.

## Features

- **Waterfall Display (Spectrogram)**: Real-time visualization of frequency spectrum over time
- **Interactive Controls**: Adjust center frequency, sample rate, FFT size, and update rate
- **Signal Processing**: FFT-based frequency analysis with windowing
- **Flexible Display**: Colormap-based visualization for easy signal identification
- **Cross-platform**: Works on Linux, macOS, and Windows
- **Meshtastic Device Detection**: Automatic detection of Meshtastic devices via USB
- **LoRa Communication**: Enables LoRa communication when Meshtastic device is detected

## Installation

### Requirements

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python waverider_sdr.py
```

### Controls

The application provides the following controls:

- **Center Frequency**: Adjust the center frequency of the display (in MHz)
- **Sample Rate**: Select the sample rate (2.4 MHz, 2.048 MHz, or 1.024 MHz)
- **FFT Size**: Choose the FFT size for frequency resolution (512, 1024, 2048, 4096)
- **Update Rate**: Set the display refresh rate in milliseconds
- **Start/Stop**: Toggle signal acquisition on and off

### Meshtastic Device Status

The application displays real-time status information about Meshtastic devices:

- **Meshtastic Device**: Shows whether a Meshtastic device is detected and connected
- **LoRa Status**: Indicates if LoRa communication is enabled
  - When a Meshtastic device is detected, LoRa communication is automatically enabled at 915 MHz
  - Supported devices include RAK4631, T-Echo, Heltec Tracker, T-Beam, T-Lora, and more

### Waterfall Display

The waterfall display shows:
- **X-axis**: Frequency (in MHz)
- **Y-axis**: Time (newest data at the top)
- **Color**: Signal power in dB (darker = weaker, brighter = stronger)

The color scale ranges from -80 dB (dark) to 0 dB (bright), using the viridis colormap.

## Features in Detail

### Real-time Signal Visualization

The waterfall display updates in real-time, showing how the frequency spectrum changes over time. This is essential for:
- Identifying signal patterns
- Monitoring frequency activity
- Detecting intermittent signals
- Analyzing signal characteristics

### Signal Processing

The application performs the following signal processing:
1. Captures IQ samples from the signal source
2. Applies Hamming window to reduce spectral leakage
3. Computes FFT to convert to frequency domain
4. Converts magnitude to dB scale
5. Updates waterfall display with new data

### Demonstration Mode

Currently, the application uses a simulated signal generator that creates:
- Multiple carrier signals at different frequencies
- FM-like modulated signals
- Background noise

This allows you to see the waterfall visualization in action without requiring actual SDR hardware.

## Future Enhancements

- Support for real SDR hardware (RTL-SDR, HackRF, etc.)
- Recording and playback functionality
- Signal demodulation
- Frequency bookmarks
- Adjustable colormap and dynamic range
- Advanced LoRa packet capture and analysis
- Meshtastic message monitoring and transmission

## License

See LICENSE file for details. 
