# table.py

import pygame
from datetime import datetime, timedelta
from config import FONT_PATH, DATA, BLACK_COLOR, RED_COLOR, FOREST_GREEN_COLOR
from utils import apply_manual_override, format_time, calculate_iqamah, render_centered
from countdown import get_next_prayer

from test import set_datetime # Temporary: Testing function

def format_prayer_table(prayer_times):
    """Format prayer times into a table."""
    
    if not prayer_times:
        prayer_times = {}
    
    prayers = [
        ("Fajr", "Fajr"),
        ("Sunrise", "Sunrise"),
        ("Dhuhr", "Dhuhr"),
        ("Asr", "Asr"),
        ("Maghrib", "Maghrib"),
        ("Isha", "Isha"),
    ]
    
    prayer_data = prayer_times
    formatted_prayer_times = []
    
    PLACEHOLDER = "––––––––––"
    
    for prayer_name, csv_key in prayers:
        
        api_time = prayer_data.get(csv_key, '')
        adhan_time = format_time(apply_manual_override(prayer_name, api_time))
        iqamah_time = PLACEHOLDER
        
        # Calculate Iqamah time
        if adhan_time != PLACEHOLDER:
            iqamah_time = calculate_iqamah(adhan_time, prayer_name)
            if not iqamah_time:
                iqamah_time = PLACEHOLDER
        
        formatted_prayer_times.append((prayer_name, adhan_time, iqamah_time))
    
    # Handle Jummah
    jummah = DATA['JUMMAH']
    jummah_adhan = jummah.get('ADHAN_TIME', '').strip()
    
    if prayer_times and jummah_adhan:
        jummah_iqamah_time = calculate_iqamah(jummah_adhan, "Jummah")
        if not jummah_iqamah_time:
            jummah_iqamah_time = PLACEHOLDER
        
        formatted_prayer_times.append(("Jummah", jummah_adhan, jummah_iqamah_time))
    else:
        formatted_prayer_times.append(("Jummah", PLACEHOLDER, PLACEHOLDER))
    
    return formatted_prayer_times

def render_prayer_table(screen, prayer_table, scale_x, scale_y):
    """Render the prayer times table."""
    
    font_size = int(63 * scale_y)
    table_font = pygame.font.Font(FONT_PATH, font_size)
    
    table_start_x, table_start_y = int(46 * scale_x), int(252 * scale_y)
    vertical_spacing = int(font_size * 1.2)
    col_widths = [int(170 * scale_x), int(275 * scale_x), int(186 * scale_x)]
    
    next_prayer, _, _ = get_next_prayer(set_datetime()) # Temporary: Use test mode datetime
    
    # Calculate starting x-positions for each column
    col_positions = [table_start_x,
            table_start_x + col_widths[0],
            table_start_x + col_widths[0] + col_widths[1]]
    
    # Render header
    for col_idx, header_text in enumerate(["", "Adhan", "Iqamah"]):
        render_centered(screen, header_text, FOREST_GREEN_COLOR, col_positions, col_widths, table_font, col_idx, table_start_y)
    
    # Render prayer rows
    for i, (prayer_name, adhan, iqamah) in enumerate(prayer_table):
        y = table_start_y + ((i + 1) * vertical_spacing)
        
        if prayer_name == next_prayer:
            color = RED_COLOR
        else:
            color = BLACK_COLOR
        
        screen.blit(table_font.render(prayer_name, True, FOREST_GREEN_COLOR), (col_positions[0], y))  # Left-justified
        render_centered(screen, adhan, color, col_positions, col_widths, table_font, 1, y)
        render_centered(screen, iqamah, color, col_positions, col_widths, table_font, 2, y)