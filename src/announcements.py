# announcements.py

from config import ANNOUNCEMENTS, BLACK_COLOR, RED_COLOR, FOREST_GREEN_COLOR

def render_announcements(screen, scale_x, scale_y, title_font, detail_font):
    """Render announcements."""
    
    if not ANNOUNCEMENTS:
        return
    
    # Render header
    announcement_header_surface = title_font.render("Announcement:", True, RED_COLOR)
    announcement_header_rect = announcement_header_surface.get_rect(center=(int(1090 * scale_x), int(294 * scale_y)))
    screen.blit(announcement_header_surface, announcement_header_rect)
    
    # Render announcements
    for i, text in enumerate(ANNOUNCEMENTS):
        
        x = int(907 * scale_x)
        y = int((343 + i * 48) * scale_y)
        
        before, after = text.split(':', 1)

        # Render before colon
        before_surface = detail_font.render(f"-      {before.strip()}", True, FOREST_GREEN_COLOR)
        before_rect = before_surface.get_rect(topleft=(x, y))
        screen.blit(before_surface, before_rect)

        # Render after colon
        after_surface = detail_font.render(f": {after.strip()[:26]}", True, BLACK_COLOR)
        after_rect = after_surface.get_rect(topleft=(before_rect.right, y))
        screen.blit(after_surface, after_rect)