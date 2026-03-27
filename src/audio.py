# audio.py

import wave
import numpy as np
from src.config import BEEP

def generate_beep(frequency=1000, duration=1.0, volume=0.1, sample_rate=22050):
    """Generate a beep sound using a sine wave and save to a WAV file."""
    
    # Calculate total frames for the given duration
    frames = int(duration * sample_rate)
    
    # Generate sine wave
    t = np.linspace(0, duration, frames, endpoint=False)
    waveform = np.sin(2 * np.pi * frequency * t)
    
    # Scale to 16-bit audio with volume control
    amplitude = int(32767 * volume)
    waveform = (waveform * amplitude).astype(np.int16)
    
    # Create stereo (2 channels)
    stereo = np.column_stack((waveform, waveform))
    
    # Save to WAV file
    with wave.open(BEEP, "wb") as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(stereo.tobytes())
        print("Beep file generated.")

if __name__ == "__main__":
    generate_beep()