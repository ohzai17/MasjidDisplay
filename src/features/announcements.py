# announcements.py

from src.utils import load_settings, get_text_colors, render_text

def render_announcements(screen, scale_x, scale_y, title_font, detail_font):
    """Render announcements."""
    
    settings = load_settings()
    
    DISPLAY = settings['DISPLAY']
    ANNOUNCEMENTS = DISPLAY['ANNOUNCEMENTS']
    
    primary, secondary, tertiary = get_text_colors()
    
    # Render header
    render_text(
        screen, "Announcement:", title_font, primary,
        (int(1206 * scale_x), int(659 * scale_y)),
        align="center", shadow_color=tertiary
    )
    
    # Render announcements
    for i, text in enumerate(ANNOUNCEMENTS[:3]):
        x = int(877 * scale_x)
        y = int((733 + i * 48) * scale_y)
        
        # Render dash
        dash = render_text(
            screen, "-", detail_font, 
            secondary, (x, y), align="left",
            shadow_color=tertiary
        )
        
        # Render announcement text
        if ':' in text:
            before, after = text.split(':', 1)
            before = render_text(
                screen, f"      {before.strip()}", detail_font,
                primary, (dash.right, y), align="left",
                shadow_color=tertiary
            )
            render_text(
                screen, f": {after.strip()[:26]}", detail_font,
                secondary, (before.right, y), align="left",
                shadow_color=tertiary
            )
        else:
            render_text(
                screen, f"      {text.strip()[:38]}", detail_font,
                secondary, (dash.right, y), align="left",
                shadow_color=tertiary
            )