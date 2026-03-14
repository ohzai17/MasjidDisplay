# background.py

import pygame
from src.config import TEXTURE, WHITE, BLACK
from src.utils import load_prayer_times

def render_background(screen):
    """Render the background."""
    
    prayer_times = load_prayer_times()
    
    if prayer_times:
        screen.fill(BLACK)
        background = pygame.image.load(TEXTURE).convert_alpha()
        background = pygame.transform.smoothscale(background, (screen.get_width(), screen.get_height()))
        screen.blit(background, (0, 0))
    else:
        screen.fill(WHITE)