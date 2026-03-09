# background.py

from src.config import WHITE, THEMES
from src.utils import load_prayer_times

def render_background(screen, theme_index):
    """Render the background."""
    
    prayer_times = load_prayer_times()
    
    if prayer_times:
        color = THEMES[theme_index]["BACKGROUND"]
    else:
        color = WHITE
    
    screen.fill(color)