# main.py

import pygame
from datetime import datetime
from hijridate import Gregorian
from config import (
    FONT_PATH, HIJRI_MONTH_NAMES, FPS, WIDTH, HEIGHT, FULLSCREEN, DESIGN_WIDTH,
    DESIGN_HEIGHT, NAME, ADDRESS, BLACK_COLOR, WHITE_COLOR, FOREST_GREEN_COLOR
)
from test import set_datetime, advance_time # Temporary: Testing functions
from utils import get_prayer_times, get_seconds
from background import get_gradient_colors, render_gradient
from table import format_prayer_table, render_prayer_table
from countdown import render_countdown
from announcements import render_announcements

# Temporary: Enable test mode and set test time
TEST_MODE = True
test_time = datetime(2025, 12, 25, 6, 35, 57) # (year, month, day, hour, minute, second)

def main():
    
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption(NAME)
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if FULLSCREEN else 0)
    
    width = screen.get_width()
    height = screen.get_height()
    
    clock = pygame.time.Clock()
    
    # Calculate scale factors
    scale_x = width / DESIGN_WIDTH
    scale_y = height / DESIGN_HEIGHT
    
    # Load fonts
    time_font = pygame.font.Font(FONT_PATH, int(130 * scale_y))
    title_font = pygame.font.Font(FONT_PATH, int(85 * scale_y))
    detail_font = pygame.font.Font(FONT_PATH, int(40 * scale_y))
    
    running = True
    show_announcements = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                show_announcements = not show_announcements
        
        # Temporary: Moved for test datetime
        prayer_times = get_prayer_times()
        prayer_table = format_prayer_table(prayer_times)
        prayer_times_seconds = get_seconds(prayer_times)
        
        # Get the current date and time
        current_datetime = set_datetime() # Temporary: Use test mode datetime
        current_seconds = current_datetime.hour * 3600 + current_datetime.minute * 60 + current_datetime.second # Seconds since midnight
        time_str = current_datetime.strftime("%I:%M:%S %p")
        date_str = current_datetime.strftime("%d %B %Y")
        
        # Get the Hijri date
        hijri_date = Gregorian(current_datetime.year, current_datetime.month, current_datetime.day).to_hijri()
        hijri_month_name = HIJRI_MONTH_NAMES[hijri_date.month]
        hijri_str = f"{hijri_date.day:02d} {hijri_month_name} {hijri_date.year}"
        
        dates = date_str + " · " + hijri_str # Combine Gregorian and Hijri dates
        
        name_surface = title_font.render(NAME, True, FOREST_GREEN_COLOR)
        address_surface = detail_font.render(ADDRESS, True, BLACK_COLOR)
        time_surface = time_font.render(time_str, True, BLACK_COLOR)
        date_surface = detail_font.render(dates, True, FOREST_GREEN_COLOR)
        
        name_rect = name_surface.get_rect(center=(int(1217 * scale_x), int(98 * scale_y)))
        address_rect = address_surface.get_rect(center=(int(1217 * scale_x), int(169 * scale_y)))
        time_rect = time_surface.get_rect(center=(int(363 * scale_x), int(174 * scale_y)))
        date_rect = date_surface.get_rect(center=(int(363 * scale_x), int(68 * scale_y)))
        
        # Render background
        if prayer_times_seconds:
            top_color, bottom_color = get_gradient_colors(current_seconds, prayer_times_seconds)
            render_gradient(screen, top_color, bottom_color)
        else:
            screen.fill(WHITE_COLOR)
        
        screen.blit(name_surface, name_rect)
        screen.blit(address_surface, address_rect)
        screen.blit(time_surface, time_rect)
        screen.blit(date_surface, date_rect)
        
        render_prayer_table(screen, prayer_table, scale_x, scale_y)
        render_countdown(screen, scale_x, scale_y, title_font, time_font)
        
        if show_announcements:
            render_announcements(screen, scale_x, scale_y, title_font, detail_font)
        
        pygame.display.flip()
        clock.tick(FPS)
        
        # Temporary: Advance test time
        if TEST_MODE:
            advance_time(seconds=1/FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()