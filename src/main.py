# main.py

import pygame
from datetime import datetime
from utils import resize_window
from display import render_main
from table import render_table
from announcements import render_announcements

# Temporary: Enable test mode and set test time
TEST_MODE = True
test_time = datetime(2026, 1, 30, 12, 29, 57)

def main():
    pygame.init()
    
    screen, scale_x, scale_y, time_font, title_font, detail_font, table_font = resize_window(window_preset=2)
    
    running = True
    show_announcements = True
    
    # Temporary: Variables for time control in test mode
    rewind = False
    fast_forward = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                window_preset = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3}[event.key]
                screen, scale_x, scale_y, time_font, title_font, detail_font, table_font = resize_window(window_preset)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                show_announcements = not show_announcements
            
            # Temporary: Time control for test mode
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                rewind = True
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                rewind = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                fast_forward = True
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                fast_forward = False
        
        screen.fill((255,255,255))
        
        render_main(screen, scale_x, scale_y, time_font, title_font, detail_font)
        render_table(screen, scale_x, scale_y, table_font)
        
        if show_announcements:
            render_announcements(screen, scale_x, scale_y, title_font, detail_font)
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)
        
        # Temporary: Advance test time
        from test import advance_time
        if TEST_MODE:
            if fast_forward:
                advance_time(seconds=50)  # Fast forward by 50 seconds per frame
            elif rewind:
                advance_time(seconds=-10) # Rewind by 10 seconds per frame
            else:
                advance_time(seconds=1/30)
    
    pygame.quit()

if __name__ == "__main__":
    main()