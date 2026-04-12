# main.py

import pygame
from src.features.table import render_table
from src.features.display import render_display
from src.utils import launch_module, setup_window
from src.features.countdown import render_countdown
from src.features.background import render_background
from src.features.announcements import render_announcements

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Masjid Display")
    pygame.mouse.set_visible(False)
    
    screen, scale_x, scale_y, clock_font, title_font, detail_font, table_font, countdown_font, arabic_font = setup_window()
    
    running = True
    show_announcements = False
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                
                # Quit on escape key and return to launcher
                if event.key == pygame.K_ESCAPE:
                    running = False
                    launch_module("src.launcher")
                
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