# utils.py

import pygame
from datetime import datetime
from config import PRESET_MAP, FONT, BLACK, NAVY_BLUE, PEACH, WHITE

def resize_window(window_preset):
    width, height, fullscreen = PRESET_MAP[window_preset]
    
    if fullscreen:
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        width = screen.get_width()
        height = screen.get_height()
    else:
        screen = pygame.display.set_mode((width, height))
    
    # Scaling factors of 1600x900 design resolution
    scale_x = width / 1600
    scale_y = height / 900
    
    time_font = pygame.font.Font(FONT, int(130 * scale_y))
    title_font = pygame.font.Font(FONT, int(85 * scale_y))
    detail_font = pygame.font.Font(FONT, int(40 * scale_y))
    table_font = pygame.font.Font(FONT, int(63 * scale_y))
    
    return screen, scale_x, scale_y, time_font, title_font, detail_font, table_font

def get_text_color(now_seconds, formatted_prayer_times):
    """Determine text color based on time of day."""
    
    sunrise = None
    maghrib = None
    
    for name, adhan, _ in formatted_prayer_times:
        if adhan == "––––––––––":
            continue
        try:
            adhan_dt = datetime.strptime(adhan, "%I:%M %p")
            seconds = adhan_dt.hour * 3600 + adhan_dt.minute * 60
            if name == "Sunrise":
                sunrise = seconds
            elif name == "Maghrib":
                maghrib = seconds
        except Exception:
            continue
    
    if sunrise is None or maghrib is None:
        return BLACK, BLACK, BLACK
    
    # Color change between 15 minutes before sunrise and 15 minutes before maghrib
    if (sunrise - 900) <= now_seconds < (maghrib - 900):
        return NAVY_BLUE, BLACK, WHITE
    else:
        return PEACH, WHITE, BLACK

def render_text(
    surface, text, font, color, pos,
    align="center",
    scale_x = 1.0, scale_y = 1.0,
    outline_color = None, outline_width = 2,
    shadow_color = None, shadow_offset = (2, 2)
):
    """Render text."""
    
    # Render text surface
    text_surface = font.render(text, True, color)
    size = (int(text_surface.get_width() * scale_x), int(text_surface.get_height() * scale_y))
    
    # Custom scaling
    if scale_x != 1.0 or scale_y != 1.0:
        text_surface = pygame.transform.smoothscale(text_surface, size)
    
    # Outline
    if outline_color and outline_width > 0:
        base = font.render(text, True, outline_color)
        if scale_x != 1.0 or scale_y != 1.0:
            base = pygame.transform.smoothscale(base, size)
        outline_surface = pygame.Surface((text_surface.get_width() + 2*outline_width, text_surface.get_height() + 2*outline_width), pygame.SRCALPHA)
        for dx in range(-outline_width, outline_width+1):
            for dy in range(-outline_width, outline_width+1):
                if dx != 0 or dy != 0:
                    outline_surface.blit(base, (dx+outline_width, dy+outline_width))
        outline_surface.blit(text_surface, (outline_width, outline_width))
        text_surface = outline_surface
    
    # Shadow
    if shadow_color:
        shadow_surface = font.render(text, True, shadow_color)
        if scale_x != 1.0 or scale_y != 1.0:
            shadow_surface = pygame.transform.smoothscale(shadow_surface, size)
        shadow_pos = (shadow_offset[0], shadow_offset[1])
        shadow_layer = pygame.Surface((text_surface.get_width() + abs(shadow_pos[0]), text_surface.get_height() + abs(shadow_pos[1])), pygame.SRCALPHA)
        shadow_layer.blit(shadow_surface, shadow_pos)
        shadow_layer.blit(text_surface, (0, 0))
        text_surface = shadow_layer
    
    # Alignment
    rect = text_surface.get_rect()
    x, y = pos
    if align == "center":
        rect.center = (x, y)
    elif align == "left":
        rect.midleft = (x, y)
    elif align == "right":
        rect.midright = (x, y)
    else:
        rect.topleft = (x, y)
    
    surface.blit(text_surface, rect)
    
    return rect