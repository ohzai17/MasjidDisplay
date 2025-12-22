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
    
    for i, text in enumerate(ANNOUNCEMENTS):
        
        y = int((343 + i * 48) * scale_y)
        
        # Render announcements
        announcement = f"-      {text[:45]}"
        announcement_surface = detail_font.render(announcement, True, RED_COLOR)
        announcement_rect = announcement_surface.get_rect(topleft=(int(907 * scale_x), y))
        screen.blit(announcement_surface, announcement_rect)