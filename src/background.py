# background.py

import pygame
from datetime import datetime
from config import GRADIENTS, BLACK, WHITE
from table import load_prayer_times, format_table

def lerp(color_start, color_end, factor):
    """Linearly interpolate between two RGB colors."""
    
    return tuple(int(a + (b - a) * factor) for a, b in zip(color_start, color_end))

def get_gradient_colors(now_seconds):
    """Determine the gradient colors based on current time and prayer times."""
    
    # Get today's formatted prayer times
    prayer_times = load_prayer_times()
    formatted_prayer_times = format_table(prayer_times)
    
    prayers = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
    PLACEHOLDER = "––––––––––"
    
    # Build a sequence of (seconds, gradient) for each prayer and night
    seq = []
    seq.append((0, GRADIENTS.get("NIGHT", [BLACK, BLACK])))  # Midnight start
    for name, adhan, _ in formatted_prayer_times:
        if name in prayers and adhan != PLACEHOLDER:
            try:
                adhan_dt = datetime.strptime(adhan, "%I:%M %p")
                seconds = adhan_dt.hour * 3600 + adhan_dt.minute * 60
                seq.append((seconds, GRADIENTS.get(name.upper(), [BLACK, BLACK])))
            except Exception:
                continue
    seq.append((86400, GRADIENTS.get("NIGHT", [BLACK, BLACK])))  # Midnight end
    seq.sort()
    
    # Use white background if there are no valid prayer times
    if len(seq) <= 2:
        return WHITE, WHITE
    
    # Find which interval now_seconds is in and interpolate colors
    for i in range(len(seq) - 1):
        start_time, start_colors = seq[i]
        end_time, end_colors = seq[i + 1]
        if start_time <= now_seconds < end_time:
            progress = (now_seconds - start_time) / (end_time - start_time) if end_time > start_time else 0
            top_color = lerp(start_colors[0], end_colors[0], progress)
            bottom_color = lerp(start_colors[1], end_colors[1], progress)
            return top_color, bottom_color
    
    return WHITE, WHITE

def draw_gradient(surface, top_color, bottom_color):
    """Render a vertical gradient on the surface."""
    
    gradient_surface = pygame.Surface((2, 2))
    pygame.draw.line(gradient_surface, top_color, (0, 0), (1, 0))
    pygame.draw.line(gradient_surface, bottom_color, (0, 1), (1, 1))
    pygame.transform.smoothscale(gradient_surface, (surface.get_width(), surface.get_height()), surface)

def render_background(screen):
    """Get current time, calculate gradient, and render background."""
    
    from test import set_datetime  # Use test time if in test mode
    now = set_datetime()
    
    now_seconds = now.hour * 3600 + now.minute * 60 + now.second
    top_color, bottom_color = get_gradient_colors(now_seconds)
    draw_gradient(screen, top_color, bottom_color)