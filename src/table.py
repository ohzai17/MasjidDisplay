# table.py

import pygame
from datetime import datetime
from config import FONT_PATH, BLACK_COLOR, RED_COLOR, FOREST_GREEN_COLOR
from utils import get_next_prayer

def render_prayer_table(screen, prayer_table, scale_x, scale_y):
    """Render the prayer times table."""
    
    font_size = int(63 * scale_y)
    table_font = pygame.font.Font(FONT_PATH, font_size)
    
    table_start_x, table_start_y = int(46 * scale_x), int(252 * scale_y)
    vertical_spacing = int(font_size * 1.2)
    col_widths = [int(170 * scale_x), int(275 * scale_x), int(186 * scale_x)]
    
    next_prayer,_= get_next_prayer(datetime.now())
    
    # Calculate starting x-positions for each column
    col_positions = [table_start_x,
            table_start_x + col_widths[0],
            table_start_x + col_widths[0] + col_widths[1]]
    
    def render_centered(text, color, col, y_pos):
        """Render text centered in the specified column."""
        
        text_surface = table_font.render(text, True, color)
        x = col_positions[col] + (col_widths[col] - text_surface.get_width()) // 2
        screen.blit(text_surface, (x, y_pos))
    
    # Render header
    for col_idx, header_text in enumerate(["", "Adhan", "Iqamah"]):
        render_centered(header_text, RED_COLOR, col_idx, table_start_y)
    
    # Render prayer rows
    for i, (prayer_name, adhan, iqamah) in enumerate(prayer_table):
        y = table_start_y + ((i + 1) * vertical_spacing)
        
        if prayer_name == next_prayer:
            color = BLACK_COLOR
        else:
            color = RED_COLOR
        
        screen.blit(table_font.render(prayer_name, True, RED_COLOR), (col_positions[0], y))  # Left-justified
        render_centered(adhan, color, 1, y)
        render_centered(iqamah, color, 2, y)