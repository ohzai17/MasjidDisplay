# main.py

import pygame
from datetime import datetime
from config import (
    FONT_PATH, FPS, WIDTH, HEIGHT, FULLSCREEN, DESIGN_WIDTH,
    DESIGN_HEIGHT, NAME, WHITE_COLOR
)
from test import set_datetime, advance_time # Temporary: Testing functions
from utils import get_prayer_times, get_seconds
from background import get_gradient_colors, render_background
from table import format_prayer_table, render_prayer_table
from countdown import render_countdown
from announcements import render_announcements
from display import render_main

# Temporary: Enable test mode and set test time
TEST_MODE = True
test_time = datetime(2025, 12, 26, 6, 0, 57) # (year, month, day, hour, minute, second)

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
    table_font = pygame.font.Font(FONT_PATH, int(63 * scale_y))
    
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
        
        # Render background
        if prayer_times_seconds:
            top_color, bottom_color = get_gradient_colors(current_seconds, prayer_times_seconds)
            render_background(screen, top_color, bottom_color)
        else:
            screen.fill(WHITE_COLOR)
        
        # Render announcements
        if show_announcements:
            render_announcements(screen, scale_x, scale_y, title_font, detail_font, current_seconds, prayer_times_seconds)
        
        # Render prayer table, countdown, and main display
        render_prayer_table(screen, prayer_table, scale_x, scale_y, table_font, current_seconds, prayer_times_seconds)
        render_countdown(screen, scale_x, scale_y, title_font, time_font, current_seconds, prayer_times_seconds)
        render_main(screen, current_datetime, scale_x, scale_y, time_font, title_font, detail_font, current_seconds, prayer_times_seconds)
        
        pygame.display.flip()
        clock.tick(FPS)
        
        # Temporary: Advance test time
        if TEST_MODE:
            advance_time(seconds=1/FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()