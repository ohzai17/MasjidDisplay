# main.py

import pygame
import subprocess
from config import THEMES
from table import render_table
from display import render_main
from utils import resize_window
from countdown import render_countdown
from background import render_background
from announcements import render_announcements

def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    
    window_preset = 2
    theme_index = 0
    
    screen, scale_x, scale_y, clock_font, title_font, detail_font, table_font, countdown_font, arabic_font = resize_window(window_preset)
    
    running = True
    show_announcements = False
    
    while running:
        for event in pygame.event.get():
            # Quit on close or escape key
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                # subprocess.Popen(["python", "launcher.py"])
            elif event.type == pygame.KEYDOWN:
                # Handle window resizing
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    window_preset = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3}[event.key]
                    screen, scale_x, scale_y, clock_font, title_font, detail_font, table_font, countdown_font, arabic_font = resize_window(window_preset)
                # Toggle announcements
                elif event.key == pygame.K_a:
                    show_announcements = not show_announcements
                # Change themes
                elif event.key == pygame.K_LEFT:
                    theme_index = (theme_index - 1) % len(THEMES)
                elif event.key == pygame.K_RIGHT:
                    theme_index = (theme_index + 1) % len(THEMES)
        
        render_background(screen, theme_index)
        render_main(screen, scale_x, scale_y, clock_font, title_font, detail_font, theme_index)
        render_table(screen, scale_x, scale_y, table_font, arabic_font, theme_index)
        render_countdown(screen, scale_x, scale_y, clock_font, title_font, countdown_font, show_announcements, theme_index)
        if show_announcements:
            render_announcements(screen, scale_x, scale_y, title_font, detail_font, theme_index)
        
        pygame.display.flip()
        pygame.time.Clock().tick(15)
    
    pygame.quit()

if __name__ == "__main__":
    main()