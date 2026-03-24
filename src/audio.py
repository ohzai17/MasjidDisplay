# audio.py

import pygame
import numpy as np

def generate_beep(frequency=500, duration=1.5, volume=0.1):
    """Generate a beep sound using a sine wave."""
    
    try:
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Generate sine wave
        t = np.linspace(0, duration, frames)
        waveform = np.sin(2 * np.pi * frequency * t)
        
        # Scale to 16-bit audio with volume control
        amplitude = int(32767 * volume)
        waveform = (waveform * amplitude).astype(np.int16)
        
        # Create stereo (2 channels)
        stereo = np.zeros((frames, 2), dtype=np.int16)
        stereo[:, 0] = waveform
        stereo[:, 1] = waveform
        
        # Create pygame Sound object
        return pygame.sndarray.make_sound(stereo)
    
    except Exception:
        return None # Return None if sound generation fails