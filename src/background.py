# background.py

import pygame
from config import BACKGROUND_COLORS

def lerp(color_start, color_end, factor):
    """Linerarly interpolate between two rgb colors."""
    
    return tuple(int(a + (b - a) * factor) for a, b in zip(color_start, color_end))

def get_gradient_colors(now, prayer_times_seconds):
    """Determine the gradient colors based on current time and prayer times."""
    
    keys = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
    
    # Ensure's smooth next day transition 
    midnight_color = BACKGROUND_COLORS["NIGHT"]

    # Build the sequence
    seq = [(0, midnight_color)]
    for k in keys:
        seq.append((prayer_times_seconds[k], BACKGROUND_COLORS[k.upper()]))
    seq.append((86400, midnight_color))
    
    # Interpolate between each time interval in the sequence
    for i in range(len(seq) - 1):
        (start_time, start_colors), (end_time, end_colors) = seq[i], seq[i + 1]
        if start_time <= now <= end_time:
            # Calculate progress between the two times (0.0 = start, 1.0 = end)
            progress = (now - start_time) / (end_time - start_time) if end_time > start_time else 0
            top_color = lerp(start_colors[0], end_colors[0], progress)
            bottom_color = lerp(start_colors[1], end_colors[1], progress)
            return top_color, bottom_color
            
    return midnight_color, midnight_color

def render_gradient(surface, top_color, bottom_color):
    """Render a vertical gradient."""
    
    # Create a small 2x2 surface for the gradient
    gradient_surface = pygame.Surface((2, 2))
    
    pygame.draw.line(gradient_surface, top_color, (0, 0), (1, 0)) # Top horizontal line
    pygame.draw.line(gradient_surface, bottom_color, (0, 1), (1, 1)) # Bottom horizontal line
    
    # Scale gradient to fill the entire surface
    pygame.transform.smoothscale(
        gradient_surface, (surface.get_width(), surface.get_height()), surface)