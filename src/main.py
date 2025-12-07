# main.py

import pygame
from datetime import datetime
from hijridate import Gregorian
from config import WIDTH, HEIGHT, FULLSCREEN, FPS, BACKGROUND_COLOR, PRIMARY_COLOR, FONT_PATH, FONT_SIZE, DISPLAY, HIJRI_MONTH_NAMES

def main():
    
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if FULLSCREEN else 0)
    pygame.display.set_caption(DISPLAY['NAME'])
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BACKGROUND_COLOR)
        
        # Get current date and time
        current_datetime = datetime.now()
        
        # Render current time at the center of the screen
        time_str = current_datetime.strftime("%I:%M:%S %p")
        text_surface = font.render(time_str, True, PRIMARY_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        
        # Render current Gregorian date under the current time
        date_str = current_datetime.strftime("%B %d, %Y")
        date_surface = font.render(date_str, True, PRIMARY_COLOR)
        date_rect = date_surface.get_rect(center=(WIDTH // 2, (HEIGHT // 2) + FONT_SIZE + 10))
        screen.blit(date_surface, date_rect)
        
        # Render current Hijri date under the Gregorian date
        hijri_date = Gregorian(current_datetime.year, current_datetime.month, current_datetime.day).to_hijri()
        hijri_month_name = HIJRI_MONTH_NAMES[hijri_date.month]
        hijri_str = f"{hijri_month_name} {hijri_date.day}, {hijri_date.year}"
        hijri_surface = font.render(hijri_str, True, PRIMARY_COLOR)
        hijri_rect = hijri_surface.get_rect(center=(WIDTH // 2, (HEIGHT // 2) + 2 * FONT_SIZE + 20))
        screen.blit(hijri_surface, hijri_rect)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()