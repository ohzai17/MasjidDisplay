# announcements.py

from config import ANNOUNCEMENTS
from utils import render_text, get_text_colors

def render_announcements(screen, scale_x, scale_y, title_font, detail_font, current_seconds, prayer_times_seconds):
    """Render announcements."""
    
    if not ANNOUNCEMENTS:
        return
    
    primary_color, secondary_color, _ = get_text_colors(current_seconds, prayer_times_seconds)
    
    # Render header
    render_text(
        screen, "Announcement:", title_font, primary_color,
        (int(1217 * scale_x), int(289 * scale_y)),
        align="center"
    )
    
    # Render announcements
    for i, text in enumerate(ANNOUNCEMENTS):
        x = int(907 * scale_x)
        y = int((361 + i * 48) * scale_y)
        
        before, after = text.split(':', 1)
        
        # Render dash
        dash = render_text(
            screen, "-", detail_font, 
            secondary_color, (x, y), align="left"
        )
        
        # Render before colon
        before = render_text(
            screen, f"      {before.strip()}", detail_font,
            primary_color, (dash.right, y), align="left"
        )
        
        # Render after colon
        render_text(
            screen, f": {after.strip()[:26]}", detail_font,
            secondary_color, (before.right, y), align="left"
        )