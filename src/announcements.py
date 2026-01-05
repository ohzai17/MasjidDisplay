# announcements.py

from config import ANNOUNCEMENTS
from utils import render_text, get_text_colors

def render_announcements(screen, scale_x, scale_y, title_font, detail_font):
    """Render announcements."""
    
    primary, secondary, _ = get_text_colors()
    
    # Render header
    render_text(
        screen, "Announcement:", title_font, primary,
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
            secondary, (x, y), align="left"
        )
        
        # Render before colon
        before = render_text(
            screen, f"      {before.strip()}", detail_font,
            primary, (dash.right, y), align="left"
        )
        
        # Render after colon (cut off at 26 characters)
        render_text(
            screen, f": {after.strip()[:26]}", detail_font,
            secondary, (before.right, y), align="left"
        )