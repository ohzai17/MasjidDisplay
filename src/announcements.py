# announcements.py

from config import BLACK_COLOR, RED_COLOR, FOREST_GREEN_COLOR


def render_announcements(screen, scale_x, scale_y, title_font, detail_font):
    """Renders the announcements."""
    
    # Render header and announcements
    announcement_header_surface = title_font.render(f"Announcement:", True, RED_COLOR)
    announcement_surface = detail_font.render(f"RAMADAN BEGINS: FEBRUARY 13, 2025", True, RED_COLOR)
    
    announcement_header_rect = announcement_header_surface.get_rect(center=(int(1090 * scale_x), int(294 * scale_y)))
    announcement_rect = announcement_surface.get_rect(center=(int(1189 * scale_x), int(366 * scale_y)))
    
    screen.blit(announcement_header_surface, announcement_header_rect)
    screen.blit(announcement_surface, announcement_rect)