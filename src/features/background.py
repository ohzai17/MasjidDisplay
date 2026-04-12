# background.py

import pygame
from src.config import rgba, TEXTURE, WHITE, MIDNIGHT_BLUE, ROYAL_BLUE
from src.utils import load_prayer_times

def render_background(screen):
    """Render the background."""
    
    prayer_times = load_prayer_times()
    
    if prayer_times:
        screen.fill(MIDNIGHT_BLUE)
        background = pygame.image.load(TEXTURE).convert_alpha()
        background = pygame.transform.smoothscale(background, (screen.get_width(), screen.get_height()))
        background.fill(rgba(ROYAL_BLUE, 0), special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(background, (0, 0))
    
    else:
        screen.fill(WHITE)