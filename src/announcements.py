# announcements.py

from config import ANNOUNCEMENTS, BLACK_COLOR, FOREST_GREEN_COLOR
from utils import render_text

def render_announcements(screen, scale_x, scale_y, title_font, detail_font):
    """Render announcements."""
    
    if not ANNOUNCEMENTS:
        return
    
    # Render header
    render_text(
        screen, "Announcement:", title_font, FOREST_GREEN_COLOR,
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
            BLACK_COLOR, (x, y), align="left"
        )
        
        # Render before colon
        before = render_text(
            screen, f"      {before.strip()}", detail_font,
            FOREST_GREEN_COLOR, (dash.right, y), align="left"
        )
        
        # Render after colon
        render_text(
            screen, f": {after.strip()[:26]}", detail_font,
            BLACK_COLOR, (before.right, y), align="left"
        )