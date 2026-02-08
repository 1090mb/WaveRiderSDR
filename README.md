<div align="center">

# 🌊 WaveRider SDR

### *The only SDR with full features, rolling updates, and universal cross-platform compatibility*

[![Platform Support](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux%20%7C%20iOS%20%7C%20Android-blue.svg)](https://github.com/1090mb/WaveRiderSDR)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![SDR Support](https://img.shields.io/badge/SDR-RTL--SDR-orange.svg)](https://www.rtl-sdr.com/)

**[Quick Start](#-quick-start)** • 
**[Features](#-features)** • 
**[Installation](#-installation)** • 
**[Platform Guide](PLATFORM_GUIDE.md)** • 
**[Documentation](#-usage)**

---

</div>

## ✨ Features

<table>
<tr>
<td width="50%">

### 📡 SDR Hardware
- 🔌 Real RTL-SDR device support
- 🔍 Automatic device detection
- 🎛️ Device selection interface
- ▶️ Start/Stop controls
- 📊 Real-time signal display
- 🔄 Graceful fallback mode

</td>
<td width="50%">

### 🌐 Cross-Platform
- 💻 Windows, macOS, Linux
- 📱 iOS & Android support
---

## 🚀 Quick Start

> **Get started in seconds on any platform!**

### 🎯 Responsive design
- ⚡ Optimized codebase

</td>
</tr>
<tr>
<td width="50%">

### 📈 Visualization
- 🌈 Waterfall display (spectrogram)
- 🎨 Colormap-based visualization
- 🎚️ Interactive controls
- 🔧 Adjustable FFT parameters
- 📏 Flexible sample rates
- 🎯 Signal power indicators

</td>
<td width="50%">

### 🎵 Audio Demodulation
- 📻 Real-time audio playback
- 🔊 FM/AM/SSB demodulation
- 🎛️ Modulation selector
- 🔇 Signal detection & processing
- 🎚️ Auto audio enable/disable
- 🔉 Speaker output support

</td>
</tr>
<tr>
<td width="50%">

### 🛰️ Meshtastic & LoRa
- 📡 Meshtastic device detection
- 💬 LoRa communication support
- 🔗 USB device scanning
- 📻 915 MHz auto-tuning
- 🚀 Multiple device support
- 🎯 Automatic configuration

</td>
</tr>
</table>

## 🚀 Quick Start

### One Command - Any Platform

```bash
# Install dependencies
pip install -r requirements.txt

# Run (automatically detects your platform)
python run.py
```

That's it! WaveRider SDR will:
- ✅ Detect if you're on desktop or need web version
- ✅ Check for required dependencies  
- ✅ Launch the appropriate interface
- ✅ Work on Windows, macOS, Linux, iOS, and Android
- ✅ Automatically detect connected SDR devices
- ✅ Fall back to simulated signals if no SDR hardware present

### Using with Real SDR Hardware

To use real SDR devices (like RTL-SDR):

```bash
# Install SDR hardware support
pip install pyrtlsdr

# Run the application
python run.py

# The application will:
# 1. Automatically scan for connected SDR devices
# 2. Display detected devices in the UI
> 📱 **For mobile devices**: Start the web version on your computer, then access from your phone's browser at `http://<your-ip>:5000`

> 📖 **Detailed platform-specific instructions**: See [PLATFORM_GUIDE.md](PLATFORM_GUIDE.md)

---

## 🌍 Cross-Platform Support

<div align="center">

<table>
<tr>
<td align="center" width="33%">

### 💻 Desktop
**Windows** • **macOS** • **Linux**

Native PyQt5 GUI
<br>Full hardware support
<br>Optimized performance

</td>
<td align="center" width="33%">

### 📱 Mobile
**iOS** • **Android**

Web browser interface
---

## 📡 SDR Hardware Support

<div align="center">
✅ **RTL-SDR** (RTL2832U-based dongles)
- 🔜 **Coming Soon**: HackRF, Airspy, and more

### 🎁 Features

| Feature | Description |
|---------|-------------|
| 🔍 **Automatic Detection** | Scans for connected SDR devices on startup |
| 🎛️ **Device Selection** | Choose which SDR to use with multiple devices |
| ⚡ **Real-Time Acquisition** | Live signal processing and display |
| ⏯️ **Start/Stop Control** | Easy acquisition control |
| 🔄 **Graceful Fallback** | Simulated signals when no hardware detected |

### 🛠️ss-platform web app
<br>No installation needed
<br>Access from anywhere

</td>
</tr>
</table>

### 🔄 How It Works

WaveRider SDR provides **dual interfaces**:

| Version | Technology | Best For |
---

## 📦 Installation

### 📋 **Web Interface** | Flask + SocketIO | Mobile, tablets, remote access |

> 💡 - ✅ **iOS** (iPhone, iPad via web browser)
- ✅ **Android** (phones and tablets via web browser)

### How It Works
WaveRider SDR provides **two versions**:
1. **Desktop Application** - Native PyQt5 GUI for desktop computers
2. **Web Interface** - Browser-based interface for phones, tablets, and any device

The universal launcher (`run.py`) automatically detects your platform and starts the appropriate version!

## 📡 SDR Hardware Support

WaveRider SDR supports real SDR hardware for live signal acquisition:

### Supported Devices
- **RTL-SDR** (RTL2832U-based dongles)
- More devices coming soon (HackRF, Airspy, etc.)

### Features
- **Automatic Device Detection**: Scans for connected SDR devices on startup
- **Device Selection**: Choose which SDR to use if multiple devices are connected
- **Real-Time Acquisition**: Live signal processing and display
- **Start/Stop Control**: Start and stop signal acquisition as needed
- **Graceful Fallback**: Automatically uses simulated signals if no hardware is detected

### Setup
1.🐍 **Python 3.7+**
- 📦 **pip** package manager
- 🌐 **Internet connection** (for initial setup)

### ⚡Select your device from the dropdown menu
6. Click "Start" to begin signal acquisition

## Installation

### Requirements

- Python 3.7 or higher
- pip package manager
- Internet connection (for initial dependency installation)

### Quick Start (Recommended)

The easiest way to run WaveRider SDR on **any platform**:

```bash
# Install core dependencies
pip install -r requirements.txt
🔧 Manual Installation

<details>
<summary>Click to expand manual installation options</summary>

#### 🖥️
The launcher will:
1. Detect your operating system and capabilities
2. Check for required dependencies
3. Offer to install any missing dependencies
4. Launch the appropriate version for your device

### Manual Installation

If yo🌐 u prefer to manually choose which version to install:

#### For Desktop (Windows, macOS, Linux with GUI):

```bash
# Install desktop dependencies
pip install numpy matplotlib scipy PyQt5 pyserial

# Run desktop version
python waverider_sdr.py
```

#### For Web/Mobile (Any device with a browser):

```bash
# Install web dependencies  
pip install numpy matplotlib scipy flask flask-socketio pyserial
🖥️ **On the same device**: `http://localhost:5000`
- 📱 **From other devices**: `http://<your-ip-address>:5000`

#### 🔍

- **Windows**: `ipconfig` in Command Prompt  
- **macOS/Linux**: `ifconfig` or `ip addr` in Terminal  
- **Look for**: IPv4 address (usually `192.168.x.x` or `10.x.x.x`)

</details>

---🚀 

## 🎮# Finding Your IP Address

**Windows**: `ipconfig` in Command Prompt  
**macOS/Linux**: `ifconfig` or `ip addr` in Terminal  
**Optional flags:**
| Flag | Description |
|------|-------------|
| `--web` or `-w` | Force web version |
| `--desktop` or `-d` | Force desktop version |
| `--help` or `-h` | Show help |

### 🎯 Running Specific Versions

#### 🖥️on run.py
```

The launcher supports optional flags:
- `py🌐 thon run.py --web` or `python run.py -w` - Force web version
- `python run.py --desktop` or `python run.py -d` - Force desktop version
- `python run.py --help` or `python run.py -h` - Show help

### Running Specific Versions

#### Desktop Application:

```bash
pyth📱 on waverider_sdr.py
```

#### Web Interface:

```bash
python waverider_web.py
```

### Accessing on Mobile Devices

1. Start the web version on your computer:
   ```bash
   python waverider_web.py
   ```

2. F🎛️ ind your computer's IP address (e.g., 192.168.1.100)

3. On your phone/tablet browser, navigate to:
   ```
| Control | Description | Options |
|---------|-------------|---------|
| 📻 **Center Frequency** | Adjust center frequency | In MHz |
| 📊 **Sample Rate** | Select sample rate | 2.4 MHz, 2.048 MHz, 1.024 MHz |
| 📈 **FFT Size** | Frequency resolution | 512, 1024, 2048, 4096 |
| ⏱️ **Update Rate** | Display refresh rate | In milliseconds |
| ⏯️ **Start/Stop** | Toggle acquisition | On/Off |
| 🎚️ **Modulation** | Demodulation mode | FM, AM, USB, LSB |
| 🔊 **Audio Enable** | Enable audio output | Checkbox |

### 🎵 Audio Demodulation & Playback

WaveRider SDR now features **real-time audio demodulation and playback**! When you click Start and enable audio, the application will:

1. 🔍 **Detect Signals** - Automatically detect signals above -40 dB threshold
2. 🎛️ **Demodulate** - Process signals using selected modulation (FM/AM/SSB)
3. 🔊 **Play Audio** - Output demodulated audio through your speakers in real-time

**Supported Modulation Modes:**

| Mode | Full Name | Best For | Characteristics |
|------|-----------|----------|-----------------|
| **FM** | Frequency Modulation | Broadcast radio, NFM comms | Wide bandwidth, high quality |
| **AM** | Amplitude Modulation | AM radio, aviation | Simple, good for voice |
| **USB** | Upper Sideband | Ham radio, HF comms | Efficient, narrow bandwidth |
| **LSB** | Lower Sideband | Ham radio, HF comms | Efficient, narrow bandwidth |

**How to Use:**
1. Click **Start** button to begin acquisition
2. Check **"Enable Audio Output"** checkbox
3. Select your desired **modulation mode** from dropdown
4. Tune to a frequency with an active signal
5. Audio will automatically play when signal strength is sufficient!

> 💡 **Tip**: For best results with broadcast FM, use wideband FM mode and tune to 88-108 MHz. For voice communications, try AM or SSB modes.

> ⚠️ **Requirement**: Audio playback requires `sounddevice` library. Install with: `pip install sounddevice`

### 📡 Meshtastic Device Status
- **Center Frequency**: Adjust the center frequency of the display (in MHz)
Real-time monitoring of Meshtastic devices:

| Indicator | Status | Details |
|-----------|--------|---------|
| 🔌 **Device** | Detection status | Shows if Meshtastic device is connected |
| 📡 **LoRa** | Communication status | Auto-enabled at 915 MHz when device detected |
| 🛰️ **Supported Devices** | Compatible hardware | RAK4631, T-Echo, Heltec Tracker, T-Beam, T-Lora, and more |

### 🌊 application displays real-time status information about Meshtastic devices:
| Axis | Represents | Details |
|------|------------|---------|
| **X-axis** | Frequency | In MHz |
| **Y-axis** | Time | Newest data at top |
| **Color** | Signal power | -80 dB (dark) to 0 dB (bright) |

> 🎨 Uses the **viridis colormap** for optimal visibility

---

## 🔬 Features in Detail
frequency spectrum changes:

| Capability | Use Case |
|------------|----------|
| 🔍 **Pattern Identification** | Spot signal patterns instantly |
| 📈 **Frequency Monitoring** | Track activity across bands |
| ⚡ **Intermittent Detection** | Catch brief signals |
| 🔬 **Signal Analysis** | Analyze characteristics |
**Processing Pipeline:**

```
📡 IQ Samples → 🪟 Hamming Window → 📊 FFT → 📉 dB Scale → 🌊 Waterfall Display
```

1. **Capture** IQ samples from signal source
2. **Apply** Hamming window (reduces spectral leakage)
3. **Compute** FFT (time → frequency domain)
Test without hardware! The simulated signal generator creates:

- 📻 Multiple carrier signals at different frequencies
- 🎵 FM-like modulated signals
- 🌫️ Background noise for realism

> 💡 Perfect for testing the waterfall visualization without SDR hardware

---
🖥️ Desktop Version | 🌐 Web Version | 📝 Notes |
|----------|:-----------------:|:-------------:|---------|
| **Windows 7+** | ✅ | ✅ | Both Qt and web versions work |
| **macOS 10.14+** | ✅ | ✅ | Both Qt and web versions work |
| **Linux (Desktop)** | ✅ | ✅ | Both versions fully supported |
| **Linux (Server/Headless)** | ❌ | ✅ | Web version recommended |
| **iOS (iPhone/iPad)** | ❌ | ✅ | Use Safari/Chrome browser |
| **Android (Phones/Tablets)** | ❌ | ✅ | Use any modern browser |
| **Raspberry Pi** | ⚠️ | ✅ | Web version recommended |
| **Chromebook** | ❌ | ✅ | Web version only |

### 🌐 Demonstration Mode

| Browser | Platform | Status |
|---------|----------|:------:|
| 🌐 **Chrome/Chromium** | Desktop & Mobile | ✅ |
| 🦊 **Firefox** | Desktop & Mobile | ✅ |
| 🧭 **Safari** | macOS & iOS | ✅ |
| 🌊 **Edge** | Windows | ✅ |
| 📱 **Samsung Internet** | Android | ✅ |
| 🎭 **Opera** | All platforms | ✅ |

**Minimum Requirements:** HTML5 • WebSocket • JavaScript enabled

### 🔗*Linux (Ubuntu, Debian, etc.)** | ✅ Full Support | ✅ Full Support | Both versions supported |
| **Linux (Server/Headless)** | ❌ No Display | ✅ Full Support | Web version recommended |
| **iOS (iPhone/iPad)** | ❌ No Qt Support | ✅ Full Support | Use web version via Safari/Chrome |
| **Android (Phones/Tablets)** | ❌ No Qt Support | ✅ Full Support | Use web version via any browser |
<details>
<summary>Click to expand network configuration steps</summary>

#### Step 1: Same WiFi Network 📶
Ensure both the computer running the server and your mobile device are connected to the same WiFi network.

#### Step 2: Firewall Configuration 🔥

**Windows** (restrict to local network):
```powershell
netsh advfirewall firewall add rule name="WaveRider SDR" dir=in action=allow protocol=TCP localport=5000 remoteip=localsubnet
```

**macOS**:
- System Preferences → Security & Privacy → Firewall → Firewall Options → Add Python application

**Linux** (UFW - restrict to local network):
```bash
sudo ufw allow from 192.168.0.0/16 to any port 5000 proto tcp
sudo ufw allow from 10.0.0.0/8 to any port 5000 proto tcp
```
---

## 🔒 Security Best Practices

> Keeping your WaveRider SDR installation secure

| Practice | Description | Recommendation |
|----------|-------------|----------------|
| 🏠 **Local Network Only** | Default binds to 0.0.0.0 | ✅ Safe on trusted networks |
| 🔥 **Firewall Rules** | Restrict to local ranges | ✅ Use 192.168.x.x, 10.x.x.x |
```
📁 WaveRiderSDR/
│
├── 🚀 run.py                    # Universal launcher (auto-detects platform)
├── 🖥️ waverider_sdr.py          # Desktop GUI application (PyQt5)
├── 🌐 waverider_web.py          # Web interface (Flask + SocketIO)
├── 🔧 waverider_common.py       # Shared utilities and classes
│   ├── 📡 MeshtasticDetector    # USB device detection
│   ├── 📻 LoRaCommunication     # LoRa communication management
│   ├── 🎛️ SignalGenerator       # Simulated RF signal generation
│   └── 📊 compute_fft_db()      # Optimized FFT computation
│
├── 📄 templates/
│   └── index.html               # Web interface template
│
├── 📋 requirements.txt          # Python dependencies
├── 📖 README.md                 # This file
├── 🗺️ PLATFORM_GUIDE.md         # Detailed platform instructions
└── 📝 IMPLEMENTATION_SUMMARY.md # Technical implementation details
```

### ⚡**macOS**: System Preferences → Security & Privacy → Firewall → Firewall Options → Add Python application
| Optimization | Benefit |
|--------------|---------|
| 🔧 **Shared Code Module** | Eliminated duplication via `waverider_common.py` |
| ⚡ **Optimized FFT** | Centralized computation with Hamming windowing |
| 🎛️ **Efficient Signal Gen** | Reusable generator for both interfaces |
| 🛡️ **Graceful Dependencies** | Optional imports with clear error messages |

---

## 🚀 Future Enhancements

<table>
<tr>
<td width="50%">

### 🎯 Recently Added
- ✅ RTL-SDR device support
- ✅ Audio demodulation (FM, AM, SSB)
- ✅ Real-time audio playback
- ✅ Signal detection & processing

### 🔜 In Development
- 🔜 Additional SDR hardware (HackRF, Airspy)
- 🔜 Recording and playback functionality

</td>
<td width="50%">

### 💡 Planned Features
- 📑 Frequency bookmarks
- 🎨 Adjustable colormap & dynamic range
- 📡 Advanced LoRa packet analysis
- 💬 Meshtastic message monitoring

</td>
</tr>
</table>

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

### 🌟 Made with ❤️ by the WaveRider SDR Team

**[Report Bug](https://github.com/1090mb/WaveRiderSDR/issues)** • 
**[Request Feature](https://github.com/1090mb/WaveRiderSDR/issues)** • 
**[Documentation](PLATFORM_GUIDE.md)**

---

*Universal SDR for everyone, everywhere* 🌊📡

</div>

WaveRider SDR is built with a modular architecture for maintainability and code reuse:

```
WaveRiderSDR/
├── run.py                    # Universal launcher (auto-detects platform)
├── waverider_sdr.py          # Desktop GUI application (PyQt5)
├── waverider_web.py          # Web interface (Flask + SocketIO)
├── waverider_common.py       # Shared utilities and classes
│   ├── MeshtasticDetector    # USB device detection
│   ├── LoRaCommunication     # LoRa communication management
│   ├── SignalGenerator       # Simulated RF signal generation
│   └── compute_fft_db()      # Optimized FFT computation
├── templates/
│   └── index.html            # Web interface template
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── PLATFORM_GUIDE.md         # Detailed platform instructions
└── IMPLEMENTATION_SUMMARY.md # Technical implementation details
```

### Key Optimizations

- **Shared Code Module**: Common classes moved to `waverider_common.py` to eliminate duplication
- **Optimized FFT Processing**: Centralized FFT computation with Hamming windowing
- **Efficient Signal Generation**: Reusable signal generator for both interfaces
- **Graceful Dependency Handling**: Optional imports with informative error messages

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 
