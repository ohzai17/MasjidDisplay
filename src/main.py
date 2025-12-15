# main.py

import pygame
from datetime import datetime
from hijridate import Gregorian
from config import FPS, WIDTH, HEIGHT, FULLSCREEN, FONT_PATH, NAME, ADDRESS, BLACK_COLOR, WHITE_COLOR, FOREST_GREEN_COLOR, HIJRI_MONTH_NAMES

def main():
    
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if FULLSCREEN else pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(NAME)
    
    width = screen.get_width()
    height = screen.get_height()
    
    clock = pygame.time.Clock()
    
    mockup = pygame.image.load('assets/mockup.jpg') # Temporary: Load background mockup image
    
    font_size = 35
    font = pygame.font.Font(FONT_PATH, font_size)
    
    running = True
    show_background = False # Temporary: Toggle for background display
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                
        # Temporary: Toggle background with 'b' key            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                show_background = not show_background
        if show_background:
            screen.blit(mockup, (0, 0))
        else:
            screen.fill(WHITE_COLOR)
        
        # Get the current date and time
        current_datetime = datetime.now()
        time_str = current_datetime.strftime("%I:%M:%S %p")
        date_str = current_datetime.strftime("%B %d, %Y")
        
        # Get the Hijri date
        hijri_date = Gregorian(current_datetime.year, current_datetime.month, current_datetime.day).to_hijri()
        hijri_month_name = HIJRI_MONTH_NAMES[hijri_date.month]
        hijri_str = f"{hijri_month_name} {hijri_date.day}, {hijri_date.year}"
        
        # Render the masjid name at the vertical center
        name_surface = font.render(NAME, True, BLACK_COLOR)
        name_rect = name_surface.get_rect(center=(width // 2, height // 2))
        screen.blit(name_surface, name_rect)
        
        # Render the address below the masjid name
        address_surface = font.render(ADDRESS, True, BLACK_COLOR)
        address_rect = address_surface.get_rect(center=(width // 2, (height // 2) + font_size + 10))
        screen.blit(address_surface, address_rect)
        
        # Render the current time below the address
        text_surface = font.render(time_str, True, BLACK_COLOR)
        text_rect = text_surface.get_rect(center=(width // 2, (height // 2) + 2 * font_size + 20))
        screen.blit(text_surface, text_rect)
        
        # Render the Gregorian date below the time
        date_surface = font.render(date_str, True, BLACK_COLOR)
        date_rect = date_surface.get_rect(center=(width // 2, (height // 2) + 3 * font_size + 30))
        screen.blit(date_surface, date_rect)
        
        # Render the Hijri date below the Gregorian date
        hijri_surface = font.render(hijri_str, True, BLACK_COLOR)
        hijri_rect = hijri_surface.get_rect(center=(width // 2, (height // 2) + 4 * font_size + 40))
        screen.blit(hijri_surface, hijri_rect)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()