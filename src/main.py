# main.py

import pygame
from datetime import datetime
from config import WIDTH, HEIGHT, FULLSCREEN, FPS, BACKGROUND_COLOR, PRIMARY_COLOR, FONT_PATH, FONT_SIZE, DISPLAY
from utils import render_text_centered

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

        # Get current time
        current_time = datetime.now()
        time_str = current_time.strftime("%I:%M:%S %p")

        # Render time
        render_text_centered(screen, time_str, font, PRIMARY_COLOR, center=(WIDTH // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()

if __name__ == "__main__":
    main()