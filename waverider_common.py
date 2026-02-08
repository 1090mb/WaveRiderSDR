"""
WaveRiderSDR Common Module
Shared classes and utilities used by both desktop and web versions
"""

import numpy as np

# Check for pyserial availability
try:
    import serial.tools.list_ports
    PYSERIAL_AVAILABLE = True
except ImportError:
    PYSERIAL_AVAILABLE = False

# Check for RTL-SDR support
try:
    from rtlsdr import RtlSdr
    RTLSDR_AVAILABLE = True
except ImportError:
    RTLSDR_AVAILABLE = False

# Check for audio output support
try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
    AUDIO_BACKEND = 'sounddevice'
except ImportError:
    try:
        import pyaudio
        AUDIO_AVAILABLE = True
        AUDIO_BACKEND = 'pyaudio'
    except ImportError:
        AUDIO_AVAILABLE = False
        AUDIO_BACKEND = None

from scipy import signal as scipy_signal


class SDRDevice:
    """Interface for SDR devices (RTL-SDR, HackRF, etc.)
    
    This class provides a unified interface for detecting and reading from
    various SDR hardware devices.
    """
    
    def __init__(self):
        """Initialize SDR device interface"""
        self.device = None
        self.device_type = None
        self.is_connected = False
        self.sample_rate = 2.4e6
        self.center_freq = 100e6
        self.gain = 'auto'
        self.lna_gain = 0  # Low Noise Amplifier gain
        self.vga_gain = 0  # Variable Gain Amplifier gain
        self.if_gain = 0   # Intermediate Frequency gain
        self.available_gains = []
        
    def detect_devices(self):
        """Detect available SDR devices
        
        Returns:
            list: List of detected SDR devices with their info
        """
        devices = []
        
        # Check for RTL-SDR devices
        if RTLSDR_AVAILABLE:
            try:
                # Try to get device count
                from rtlsdr import librtlsdr
                device_count = librtlsdr.rtlsdr_get_device_count()
                
                for i in range(device_count):
                    name = librtlsdr.rtlsdr_get_device_name(i)
                    devices.append({
                        'index': i,
                        'type': 'RTL-SDR',
                        'name': name.decode('utf-8') if isinstance(name, bytes) else str(name),
                        'description': f'RTL-SDR Device #{i}'
                    })
            except Exception as e:
                print(f"Error detecting RTL-SDR devices: {e}")
        
        return devices
    
    def connect(self, device_index=0, device_type='RTL-SDR'):
        """Connect to an SDR device
        
        Args:
            device_index: Index of the device to connect to
            device_type: Type of device ('RTL-SDR', 'HackRF', etc.)
            
        Returns:
            bool: True if connection successful
        """
        try:
            if device_type == 'RTL-SDR' and RTLSDR_AVAILABLE:
                self.device = RtlSdr(device_index)
                self.device_type = 'RTL-SDR'
                
                # Configure device with default parameters
                self.device.sample_rate = self.sample_rate
                self.device.center_freq = self.center_freq
                self.device.gain = self.gain
                
                # Get available gains
                try:
                    self.available_gains = self.device.get_gains()
                except:
                    self.available_gains = []
                
                self.is_connected = True
                return True
            else:
                print(f"Device type {device_type} not supported or library not available")
                return False
                
        except Exception as e:
            print(f"Failed to connect to SDR device: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        """Disconnect from the SDR device"""
        if self.device:
            try:
                self.device.close()
            except Exception as e:
                print(f"Error closing SDR device: {e}")
        self.device = None
        self.is_connected = False
    
    def set_sample_rate(self, rate):
        """Set sample rate
        
        Args:
            rate: Sample rate in Hz
        """
        self.sample_rate = rate
        if self.device and self.is_connected:
            try:
                self.device.sample_rate = rate
            except Exception as e:
                print(f"Error setting sample rate: {e}")
    
    def set_center_freq(self, freq):
        """Set center frequency
        
        Args:
            freq: Center frequency in Hz
        """
        self.center_freq = freq
        if self.device and self.is_connected:
            try:
                self.device.center_freq = freq
            except Exception as e:
                print(f"Error setting center frequency: {e}")
    
    def set_gain(self, gain):
        """Set gain
        
        Args:
            gain: Gain value or 'auto'
        """
        self.gain = gain
        if self.device and self.is_connected:
            try:
                self.device.gain = gain
            except Exception as e:
                print(f"Error setting gain: {e}")
    
    def set_lna_gain(self, gain):
        """Set LNA (Low Noise Amplifier) gain
        
        Args:
            gain: LNA gain value (device-specific)
        """
        self.lna_gain = gain
        # Note: RTL-SDR doesn't have separate LNA/VGA controls
        # This is a placeholder for devices that support it
        # For RTL-SDR, we use the combined gain setting
        if self.device and self.is_connected:
            try:
                if hasattr(self.device, 'set_tuner_gain'):
                    self.device.set_tuner_gain(gain)
            except Exception as e:
                print(f"Error setting LNA gain: {e}")
    
    def set_vga_gain(self, gain):
        """Set VGA (Variable Gain Amplifier) gain
        
        Args:
            gain: VGA gain value (device-specific)
        """
        self.vga_gain = gain
        # Note: RTL-SDR doesn't have separate LNA/VGA controls
        # This is a placeholder for devices that support it
        if self.device and self.is_connected:
            try:
                if hasattr(self.device, 'set_if_gain'):
                    self.device.set_if_gain(gain)
            except Exception as e:
                print(f"Error setting VGA gain: {e}")
    
    def get_gains(self):
        """Get available gain values for the device
        
        Returns:
            list: Available gain values in dB
        """
        if self.device and self.is_connected:
            try:
                return self.device.get_gains()
            except:
                return []
        return self.available_gains
    
    def read_samples(self, num_samples):
        """Read IQ samples from the SDR device
        
        Args:
            num_samples: Number of samples to read
            
        Returns:
            numpy.ndarray: Complex IQ samples, or None if not connected
        """
        if not self.is_connected or not self.device:
            return None
        
        try:
            samples = self.device.read_samples(num_samples)
            return samples
        except Exception as e:
            print(f"Error reading samples from SDR: {e}")
            return None
    
    def get_status(self):
        """Get current SDR device status
        
        Returns:
            dict: Status information
        """
        return {
            'connected': self.is_connected,
            'device_type': self.device_type,
            'sample_rate': self.sample_rate,
            'center_freq': self.center_freq,
            'gain': self.gain
        }


class MeshtasticDetector:
    """Detect Meshtastic devices via USB
    
    This class provides cross-platform detection of Meshtastic devices
    connected via USB by checking for known vendor IDs.
    """
    
    # Known Meshtastic device vendor IDs
    MESHTASTIC_VIDS = {
        0x239a,  # RAK (RAK4631, T-Echo)
        0x303a,  # Heltec Tracker
        0x10c4,  # Silicon Labs CP210x (Heltec, T-Lora)
        0x1a86,  # WCH CH340/341 (T-Beam, T-Lora, Nano G1)
    }
    
    def __init__(self):
        """Initialize the detector"""
        self.detected_ports = []
        
    def detect_devices(self):
        """Detect Meshtastic devices connected via USB
        
        Returns:
            list: List of serial port objects for detected Meshtastic devices
        """
        if not PYSERIAL_AVAILABLE:
            return []
            
        self.detected_ports = []
        
        try:
            for port in serial.tools.list_ports.comports():
                if port.vid in self.MESHTASTIC_VIDS:
                    self.detected_ports.append(port)
        except Exception as e:
            print(f"Error detecting devices: {e}")
                
        return self.detected_ports
    
    def get_device_info(self, port):
        """Get information about a detected device
        
        Args:
            port: Serial port object
            
        Returns:
            dict: Device information including device path, VID, PID, description, and manufacturer
        """
        return {
            'device': port.device,
            'vid': hex(port.vid) if port.vid else 'N/A',
            'pid': hex(port.pid) if port.pid else 'N/A',
            'description': port.description,
            'manufacturer': port.manufacturer
        }


class LoRaCommunication:
    """Manage LoRa communication with Meshtastic devices
    
    This class handles connection and configuration of LoRa parameters
    for Meshtastic devices.
    """
    
    def __init__(self, port=None):
        """Initialize LoRa communication
        
        Args:
            port: Optional serial port device path
        """
        self.port = port
        self.serial_connection = None
        self.is_connected = False
        self.frequency = 915.0  # Default LoRa frequency in MHz (US)
        self.bandwidth = 125  # kHz
        self.spreading_factor = 7
        
    def connect(self, port):
        """Connect to a Meshtastic device
        
        Args:
            port: Serial port device path
            
        Returns:
            bool: True if connection successful
        """
        try:
            self.port = port
            # Note: Actual serial connection would be opened here
            # For now, we'll simulate the connection
            self.is_connected = True
            return True
        except Exception as e:
            print(f"Failed to connect to {port}: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        """Disconnect from the Meshtastic device"""
        if self.serial_connection:
            try:
                self.serial_connection.close()
            except Exception as e:
                print(f"Warning: Error while disconnecting from serial port: {e}")
        self.is_connected = False
        
    def configure_lora_params(self, frequency=None, bandwidth=None, spreading_factor=None):
        """Configure LoRa communication parameters
        
        Args:
            frequency: LoRa frequency in MHz (optional)
            bandwidth: Bandwidth in kHz (optional)
            spreading_factor: LoRa spreading factor 7-12 (optional)
        """
        if frequency is not None:
            self.frequency = frequency
        if bandwidth is not None:
            self.bandwidth = bandwidth
        if spreading_factor is not None:
            self.spreading_factor = spreading_factor
            
    def get_status(self):
        """Get current LoRa communication status
        
        Returns:
            dict: Status information including connection state, port, frequency, bandwidth, and spreading factor
        """
        return {
            'connected': self.is_connected,
            'port': self.port,
            'frequency': self.frequency,
            'bandwidth': self.bandwidth,
            'spreading_factor': self.spreading_factor
        }


class SignalGenerator:
    """Generate simulated SDR signals for demonstration
    
    This class creates realistic simulated RF signals with multiple carriers,
    FM modulation, and noise for testing and demonstration purposes.
    """
    
    def __init__(self, sample_rate=2.4e6, center_freq=100e6):
        """Initialize signal generator
        
        Args:
            sample_rate: Sample rate in Hz (default: 2.4 MHz)
            center_freq: Center frequency in Hz (default: 100 MHz)
        """
        self.sample_rate = sample_rate
        self.center_freq = center_freq
        self.time = 0
        
    def generate_samples(self, num_samples):
        """Generate simulated RF samples
        
        Creates a complex IQ signal with multiple components:
        - Multiple carrier waves at different frequencies
        - FM-modulated signal
        - Background noise
        
        Args:
            num_samples: Number of samples to generate
            
        Returns:
            numpy.ndarray: Complex IQ samples
        """
        # Generate time array
        t = np.arange(num_samples) / self.sample_rate + self.time
        self.time += num_samples / self.sample_rate
        
        # Create a complex signal with multiple components
        # 1. Carrier wave at center
        signal = np.exp(2j * np.pi * 0 * t)
        
        # 2. Add modulated signals at different frequencies
        signal += 0.3 * np.exp(2j * np.pi * (self.sample_rate * 0.15) * t)
        signal += 0.2 * np.exp(2j * np.pi * (self.sample_rate * -0.2) * t)
        
        # 3. Add FM-like signal
        fm_freq = self.sample_rate * 0.3
        modulation = 0.05 * np.sin(2 * np.pi * 1000 * t)
        signal += 0.4 * np.exp(2j * np.pi * fm_freq * t + modulation)
        
        # 4. Add noise
        noise = (np.random.randn(num_samples) + 1j * np.random.randn(num_samples)) * 0.1
        signal += noise
        
        return signal


def compute_fft_db(samples, fft_size=None):
    """Compute FFT and convert to dB scale
    
    Args:
        samples: Complex IQ samples
        fft_size: FFT size (optional, defaults to length of samples)
        
    Returns:
        numpy.ndarray: FFT magnitude in dB
    """
    if fft_size is None:
        fft_size = len(samples)
    
    # Apply Hamming window
    window = np.hamming(len(samples))
    samples_windowed = samples * window
    
    # Compute FFT
    fft = np.fft.fftshift(np.fft.fft(samples_windowed, n=fft_size))
    
    # Convert to dB
    magnitude = np.abs(fft)
    magnitude_db = 20 * np.log10(magnitude + 1e-10)  # Add small value to avoid log(0)
    
    return magnitude_db


class WaterfallSettings:
    """Settings and configuration for waterfall display
    
    Manages color schemes, intensity, contrast, and other waterfall parameters
    """
    
    COLORMAPS = {
        'viridis': 'viridis',
        'plasma': 'plasma',
        'inferno': 'inferno',
        'magma': 'magma',
        'hot': 'hot',
        'cool': 'cool',
        'rainbow': 'jet',
        'grayscale': 'gray',
        'turbo': 'turbo',
        'wb': 'WB'  # White-Blue (SDR++ style)
    }
    
    def __init__(self):
        """Initialize waterfall settings with defaults"""
        self.colormap = 'viridis'
        self.min_db = -80  # Minimum dB level (floor)
        self.max_db = 0    # Maximum dB level (ceiling)
        self.contrast = 1.0  # Contrast multiplier
        self.brightness = 0.0  # Brightness offset
        self.averaging = 1  # Number of frames to average (smoothing)
        self.peak_hold = False  # Enable peak hold
        self.peak_decay = 0.95  # Peak decay rate
        self.waterfall_speed = 1  # Waterfall scroll speed multiplier
        self.show_grid = True  # Show frequency grid
        self.show_peak_marker = True  # Show peak frequency marker
        
        # Peak hold buffer
        self.peak_buffer = None
    
    def set_colormap(self, colormap_name):
        """Set colormap for waterfall
        
        Args:
            colormap_name: Name of colormap from COLORMAPS
        """
        if colormap_name in self.COLORMAPS:
            self.colormap = self.COLORMAPS[colormap_name]
    
    def set_range(self, min_db, max_db):
        """Set dynamic range for waterfall
        
        Args:
            min_db: Minimum dB level
            max_db: Maximum dB level
        """
        self.min_db = min(min_db, max_db - 5)  # Ensure at least 5 dB range
        self.max_db = max_db
    
    def set_contrast(self, contrast):
        """Set contrast (0.1 to 3.0)
        
        Args:
            contrast: Contrast multiplier
        """
        self.contrast = np.clip(contrast, 0.1, 3.0)
    
    def set_brightness(self, brightness):
        """Set brightness (-50 to +50 dB)
        
        Args:
            brightness: Brightness offset in dB
        """
        self.brightness = np.clip(brightness, -50, 50)
    
    def set_averaging(self, frames):
        """Set number of frames to average for smoothing
        
        Args:
            frames: Number of frames (1 = no averaging, higher = more smoothing)
        """
        self.averaging = max(1, int(frames))
    
    def apply_processing(self, fft_db):
        """Apply waterfall processing (contrast, brightness, peak hold)
        
        Args:
            fft_db: FFT magnitude in dB
            
        Returns:
            numpy.ndarray: Processed FFT data
        """
        # Apply brightness and contrast
        processed = (fft_db + self.brightness) * self.contrast
        
        # Apply peak hold if enabled
        if self.peak_hold:
            if self.peak_buffer is None or len(self.peak_buffer) != len(processed):
                self.peak_buffer = processed.copy()
            else:
                # Update peak hold buffer
                self.peak_buffer = np.maximum(processed, self.peak_buffer * self.peak_decay)
                processed = self.peak_buffer.copy()
        
        # Clip to range
        processed = np.clip(processed, self.min_db, self.max_db)
        
        return processed
    
    def get_settings_dict(self):
        """Get all settings as dictionary
        
        Returns:
            dict: Current settings
        """
        return {
            'colormap': self.colormap,
            'min_db': self.min_db,
            'max_db': self.max_db,
            'contrast': self.contrast,
            'brightness': self.brightness,
            'averaging': self.averaging,
            'peak_hold': self.peak_hold,
            'waterfall_speed': self.waterfall_speed,
            'show_grid': self.show_grid,
            'show_peak_marker': self.show_peak_marker
        }


class AudioDemodulator:
    """Base class for audio demodulation
    
    This is the parent class for various demodulation methods (FM, AM, SSB, etc.)
    """
    
    def __init__(self, sample_rate=2.4e6, audio_rate=48000, cutoff_freq=15000, squelch_threshold=-50):
        """Initialize audio demodulator
        
        Args:
            sample_rate: Input IQ sample rate in Hz
            audio_rate: Output audio sample rate in Hz (default: 48 kHz)
            cutoff_freq: Low-pass filter cutoff frequency in Hz
            squelch_threshold: Squelch threshold in dB (default: -50 dB)
        """
        self.sample_rate = sample_rate
        self.audio_rate = audio_rate
        self.cutoff_freq = cutoff_freq
        
        # Calculate decimation factor
        self.decimation = int(sample_rate / audio_rate)
        
        # Design low-pass filter for audio
        self.audio_filter = scipy_signal.butter(5, cutoff_freq / (audio_rate / 2), btype='low')
        
        # Squelch parameters
        self.squelch_threshold = squelch_threshold  # dB threshold for squelch
        self.squelch_enabled = True
        self.squelch_alpha = 0.1  # Smoothing factor for power estimation
        self.smoothed_power = -100  # Initialize to very low value
        self.last_signal_detected = False
        self.squelch_hysteresis = 3  # dB hysteresis to prevent chattering
        
    def detect_signal(self, iq_samples):
        """Detect if there's a strong signal present (with squelch)
        
        Args:
            iq_samples: Complex IQ samples
            
        Returns:
            bool: True if signal detected above threshold
        """
        # Calculate instantaneous power in dB
        power = np.mean(np.abs(iq_samples) ** 2)
        power_db = 10 * np.log10(power + 1e-10)
        
        # Apply exponential smoothing for more stable squelch
        self.smoothed_power = (self.squelch_alpha * power_db + 
                              (1 - self.squelch_alpha) * self.smoothed_power)
        
        # Apply hysteresis to prevent chattering
        if self.squelch_enabled:
            if self.last_signal_detected:
                # Signal was on, use lower threshold to turn off
                threshold = self.squelch_threshold - self.squelch_hysteresis
            else:
                # Signal was off, use higher threshold to turn on
                threshold = self.squelch_threshold
            
            signal_detected = self.smoothed_power > threshold
        else:
            # Squelch disabled, always pass signal
            signal_detected = True
        
        self.last_signal_detected = signal_detected
        return signal_detected
    
    def set_squelch(self, threshold_db):
        """Set squelch threshold
        
        Args:
            threshold_db: Threshold in dB (-100 to 0)
        """
        self.squelch_threshold = np.clip(threshold_db, -100, 0)
    
    def enable_squelch(self, enabled):
        """Enable or disable squelch
        
        Args:
            enabled: True to enable squelch, False to disable
        """
        self.squelch_enabled = enabled
    
    def get_signal_strength(self):
        """Get current signal strength in dB
        
        Returns:
            float: Signal strength in dB
        """
        return self.smoothed_power
    
    def lowpass_filter(self, audio):
        """Apply low-pass filter to audio
        
        Args:
            audio: Audio samples
            
        Returns:
            numpy.ndarray: Filtered audio
        """
        filtered = scipy_signal.lfilter(self.audio_filter[0], self.audio_filter[1], audio)
        return filtered
    
    def demodulate(self, iq_samples):
        """Demodulate IQ samples to audio
        
        Must be implemented by subclasses
        
        Args:
            iq_samples: Complex IQ samples
            
        Returns:
            numpy.ndarray: Demodulated audio samples
        """
        raise NotImplementedError("Subclasses must implement demodulate()")


class FMDemodulator(AudioDemodulator):
    """FM (Frequency Modulation) demodulator
    
    Implements wideband FM demodulation for broadcast FM and NFM for
    narrowband communications.
    """
    
    def __init__(self, sample_rate=2.4e6, audio_rate=48000, deviation=75000):
        """Initialize FM demodulator
        
        Args:
            sample_rate: Input IQ sample rate in Hz
            audio_rate: Output audio sample rate in Hz
            deviation: FM deviation in Hz (75 kHz for broadcast, 5 kHz for NFM)
        """
        super().__init__(sample_rate, audio_rate)
        self.deviation = deviation
        self.last_phase = 0
        
    def demodulate(self, iq_samples):
        """Demodulate FM signal to audio
        
        Uses phase differentiation method for FM demodulation
        
        Args:
            iq_samples: Complex IQ samples
            
        Returns:
            numpy.ndarray: Demodulated audio samples
        """
        # Calculate instantaneous phase
        phase = np.angle(iq_samples)
        
        # Calculate phase difference (frequency)
        phase_diff = np.diff(phase, prepend=self.last_phase)
        self.last_phase = phase[-1]
        
        # Unwrap phase to handle discontinuities
        phase_diff = np.unwrap(phase_diff)
        
        # Convert to audio (scale by sample rate)
        audio = phase_diff * self.sample_rate / (2 * np.pi * self.deviation)
        
        # Decimate to audio rate
        audio_decimated = scipy_signal.decimate(audio, self.decimation, ftype='iir')
        
        # Apply de-emphasis filter (75 µs time constant for broadcast FM)
        tau = 75e-6  # Time constant
        alpha = 1 / (1 + self.audio_rate * tau)
        audio_deemph = scipy_signal.lfilter([alpha], [1, alpha - 1], audio_decimated)
        
        # Normalize audio
        audio_norm = np.clip(audio_deemph, -1, 1)
        
        return audio_norm.astype(np.float32)


class AMDemodulator(AudioDemodulator):
    """AM (Amplitude Modulation) demodulator
    
    Implements envelope detection for AM demodulation.
    """
    
    def demodulate(self, iq_samples):
        """Demodulate AM signal to audio
        
        Uses envelope detection method
        
        Args:
            iq_samples: Complex IQ samples
            
        Returns:
            numpy.ndarray: Demodulated audio samples
        """
        # Calculate envelope (magnitude)
        envelope = np.abs(iq_samples)
        
        # Remove DC component
        envelope = envelope - np.mean(envelope)
        
        # Decimate to audio rate
        audio_decimated = scipy_signal.decimate(envelope, self.decimation, ftype='iir')
        
        # Apply low-pass filter
        audio_filtered = self.lowpass_filter(audio_decimated)
        
        # Normalize
        max_val = np.max(np.abs(audio_filtered))
        if max_val > 0:
            audio_norm = audio_filtered / max_val
        else:
            audio_norm = audio_filtered
            
        return audio_norm.astype(np.float32)


class SSBDemodulator(AudioDemodulator):
    """SSB (Single Sideband) demodulator
    
    Implements USB (Upper Sideband) and LSB (Lower Sideband) demodulation.
    """
    
    def __init__(self, sample_rate=2.4e6, audio_rate=48000, mode='USB'):
        """Initialize SSB demodulator
        
        Args:
            sample_rate: Input IQ sample rate in Hz
            audio_rate: Output audio sample rate in Hz
            mode: 'USB' for upper sideband or 'LSB' for lower sideband
        """
        super().__init__(sample_rate, audio_rate, cutoff_freq=3000)
        self.mode = mode
        
        # Design bandpass filter for SSB (300 Hz to 3000 Hz)
        self.ssb_filter = scipy_signal.butter(5, [300 / (audio_rate / 2), 3000 / (audio_rate / 2)], 
                                              btype='band')
        
    def demodulate(self, iq_samples):
        """Demodulate SSB signal to audio
        
        Args:
            iq_samples: Complex IQ samples
            
        Returns:
            numpy.ndarray: Demodulated audio samples
        """
        # For SSB, we take either the real or imaginary part depending on sideband
        if self.mode == 'USB':
            audio = np.real(iq_samples)
        else:  # LSB
            audio = np.imag(iq_samples)
        
        # Decimate to audio rate
        audio_decimated = scipy_signal.decimate(audio, self.decimation, ftype='iir')
        
        # Apply SSB bandpass filter
        audio_filtered = scipy_signal.lfilter(self.ssb_filter[0], self.ssb_filter[1], 
                                              audio_decimated)
        
        # Normalize
        max_val = np.max(np.abs(audio_filtered))
        if max_val > 0:
            audio_norm = audio_filtered / max_val
        else:
            audio_norm = audio_filtered
            
        return audio_norm.astype(np.float32)


class AudioPlayer:
    """Real-time audio playback
    
    Handles audio output to speakers using sounddevice or pyaudio.
    """
    
    def __init__(self, sample_rate=48000, channels=1, buffer_size=2048):
        """Initialize audio player
        
        Args:
            sample_rate: Audio sample rate in Hz
            channels: Number of audio channels (1 for mono, 2 for stereo)
            buffer_size: Audio buffer size in samples
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.buffer_size = buffer_size
        self.is_playing = False
        self.stream = None
        
        if not AUDIO_AVAILABLE:
            print("Warning: No audio library available. Install sounddevice or pyaudio for audio playback.")
            
    def start(self):
        """Start audio playback"""
        if not AUDIO_AVAILABLE:
            return False
            
        try:
            if AUDIO_BACKEND == 'sounddevice':
                self.stream = sd.OutputStream(
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    blocksize=self.buffer_size,
                    dtype='float32'
                )
                self.stream.start()
            elif AUDIO_BACKEND == 'pyaudio':
                self.pa = pyaudio.PyAudio()
                self.stream = self.pa.open(
                    format=pyaudio.paFloat32,
                    channels=self.channels,
                    rate=self.sample_rate,
                    output=True,
                    frames_per_buffer=self.buffer_size
                )
            
            self.is_playing = True
            return True
            
        except Exception as e:
            print(f"Failed to start audio playback: {e}")
            return False
    
    def play(self, audio_data):
        """Play audio data
        
        Args:
            audio_data: Audio samples to play (numpy array)
        """
        if not self.is_playing or self.stream is None:
            return
            
        try:
            # Ensure audio data is the right type and shape
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
                
            if self.channels == 1 and len(audio_data.shape) == 1:
                # Mono audio
                if AUDIO_BACKEND == 'sounddevice':
                    self.stream.write(audio_data)
                elif AUDIO_BACKEND == 'pyaudio':
                    self.stream.write(audio_data.tobytes())
            elif self.channels == 2:
                # Stereo - duplicate mono to both channels
                if len(audio_data.shape) == 1:
                    stereo_data = np.column_stack((audio_data, audio_data))
                else:
                    stereo_data = audio_data
                    
                if AUDIO_BACKEND == 'sounddevice':
                    self.stream.write(stereo_data)
                elif AUDIO_BACKEND == 'pyaudio':
                    self.stream.write(stereo_data.tobytes())
                    
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def stop(self):
        """Stop audio playback"""
        self.is_playing = False
        
        if self.stream:
            try:
                if AUDIO_BACKEND == 'sounddevice':
                    self.stream.stop()
                    self.stream.close()
                elif AUDIO_BACKEND == 'pyaudio':
                    self.stream.stop_stream()
                    self.stream.close()
                    self.pa.terminate()
            except Exception as e:
                print(f"Error stopping audio: {e}")
                
        self.stream = None
    
    def is_active(self):
        """Check if audio is currently playing
        
        Returns:
            bool: True if audio playback is active
        """
        return self.is_playing
