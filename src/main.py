# main.py

import pygame
from src.features.table import render_table
from src.features.display import render_display
from src.utils import resize_window, launch_module
from src.features.countdown import render_countdown
from src.features.background import render_background
from src.features.announcements import render_announcements

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Masjid Display")
    pygame.mouse.set_visible(False)
    
    screen, scale_x, scale_y, clock_font, title_font, detail_font, table_font, countdown_font, arabic_font = resize_window(window_preset=1)
    
    running = True
    show_announcements = False
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            
            # Quit on close or escape key
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                launch_module("src.launcher")
            
            elif event.type == pygame.KEYDOWN:
                
                # Handle window resizing
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    preset = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3}[event.key]
                    screen, scale_x, scale_y, clock_font, title_font, detail_font, table_font, countdown_font, arabic_font = resize_window(preset)
                
                # Toggle announcements
                elif event.key == pygame.K_a:
                    show_announcements = not show_announcements
        
        render_background(screen)
        render_display(screen, scale_x, scale_y, clock_font, title_font, detail_font)
        render_table(screen, scale_x, scale_y, table_font, arabic_font)
        render_countdown(screen, scale_x, scale_y, clock_font, title_font, countdown_font, show_announcements)
        
        if show_announcements:
            render_announcements(screen, scale_x, scale_y, title_font, detail_font)
        
        pygame.display.flip()
        clock.tick(15)
    
    pygame.quit()

if __name__ == "__main__":
    main()