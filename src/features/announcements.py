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
        
        # Character limit and formatting
        announcement_text = text.strip()[:45]
        before, seperator, after = announcement_text.partition(":")
        
        # Render announcement text
        if seperator: # If there's a colon, split into two parts
            
            before_rect = render_text(
                screen, f"      {before.strip()}:", detail_font,
                primary, (dash.right, y), align="left",
                shadow_color=tertiary
            )
            render_text(
                screen, f" {after.strip()}", detail_font,
                secondary, (before_rect.right, y), align="left",
                shadow_color=tertiary
            )
        
        else:
            render_text(
                screen, f"      {announcement_text}", detail_font,
                secondary, (dash.right, y), align="left",
                shadow_color=tertiary
            )