# main.py

import pygame
import subprocess
from table import render_table
from display import render_main
from utils import resize_window
from countdown import render_countdown
from background import render_background
from announcements import render_announcements

def main():
    pygame.init()
    
    screen, scale_x, scale_y, time_font, title_font, detail_font, table_font = resize_window(window_preset=2)
    
    running = True
    show_announcements = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                subprocess.Popen(["python", "launcher.py"])
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                window_preset = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3}[event.key]
                screen, scale_x, scale_y, time_font, title_font, detail_font, table_font = resize_window(window_preset)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                show_announcements = not show_announcements
        
        render_background(screen)
        
        render_main(screen, scale_x, scale_y, time_font, title_font, detail_font)
        render_table(screen, scale_x, scale_y, table_font)
        render_countdown(screen, scale_x, scale_y, title_font, time_font)
        
        if show_announcements:
            render_announcements(screen, scale_x, scale_y, title_font, detail_font)
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)
    
    pygame.quit()

if __name__ == "__main__":
    main()