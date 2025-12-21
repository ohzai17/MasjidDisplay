# main.py

import pygame
from datetime import datetime
from hijridate import Gregorian
from config import (
    FPS, WIDTH, HEIGHT, FULLSCREEN, FONT_PATH,
    NAME, ADDRESS, BLACK_COLOR, WHITE_COLOR, RED_COLOR,
    FOREST_GREEN_COLOR, HIJRI_MONTH_NAMES
)
from table import get_prayer_times, format_prayer_table, render_prayer_table
from countdown import render_countdown

def main():
    
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption(NAME)
    
    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    width = screen.get_width()
    height = screen.get_height()
    
    clock = pygame.time.Clock()
    
    # Temporary: Load background mockup image and scale
    mockup = pygame.image.load('assets/mockup.jpg')
    mockup = pygame.transform.scale(mockup, (width, height))
    
    # Calculate scale factors
    scale_x = width / WIDTH
    scale_y = height / HEIGHT
    
    # Load fonts
    time_font = pygame.font.Font(FONT_PATH, int(130 * scale_y)) # Current time and countdown
    title_font = pygame.font.Font(FONT_PATH, int(85 * scale_y)) # Name label, announcement label, countdown label
    detail_font = pygame.font.Font(FONT_PATH, int(40 * scale_y)) # Date, Hijri date, address, and announcement details
    
    prayer_times = get_prayer_times()
    prayer_table = format_prayer_table(prayer_times)
    
    running = True
    show_background = False # Temporary: Toggle for background display
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                
        # Temporary: Toggle background with spacebar key            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                show_background = not show_background
        if show_background:
            screen.blit(mockup, (0, 0))
        else:
            screen.fill(WHITE_COLOR)
        
        # Get the current date and time
        current_datetime = datetime.now()
        time_str = current_datetime.strftime("%I:%M:%S %p")
        date_str = current_datetime.strftime("%d %B %Y")
        
        # Get the Hijri date
        hijri_date = Gregorian(current_datetime.year, current_datetime.month, current_datetime.day).to_hijri()
        hijri_month_name = HIJRI_MONTH_NAMES[hijri_date.month]
        hijri_str = f"{hijri_date.day} {hijri_month_name} {hijri_date.year}"
        
        dates = date_str + " · " + hijri_str # Combine Gregorian and Hijri dates
        
        name_surface = title_font.render(NAME, True, RED_COLOR)
        address_surface = detail_font.render(ADDRESS, True, RED_COLOR)
        time_surface = time_font.render(time_str, True, RED_COLOR)
        date_surface = detail_font.render(dates, True, RED_COLOR)
        
        name_rect = name_surface.get_rect(center=(int(1217 * scale_x), int(96 * scale_y)))
        address_rect = address_surface.get_rect(center=(int(1217 * scale_x), int(170 * scale_y)))
        time_rect = time_surface.get_rect(center=(int(363 * scale_x), int(174 * scale_y)))
        date_rect = date_surface.get_rect(center=(int(369 * scale_x), int(68 * scale_y)))
        
        screen.blit(name_surface, name_rect)
        screen.blit(address_surface, address_rect)
        screen.blit(time_surface, time_rect)
        screen.blit(date_surface, date_rect)
        
        render_prayer_table(screen, prayer_table, scale_x, scale_y)
        render_countdown(screen, scale_x, scale_y, title_font, time_font)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()