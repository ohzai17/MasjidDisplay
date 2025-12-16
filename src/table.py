# table.py

import csv
import pygame
from datetime import datetime
from config import CSV_PATH, FONT_PATH, BLACK_COLOR, RED_COLOR, FOREST_GREEN_COLOR

def get_prayer_times():
    """Load prayer times for today from the CSV file."""
    
    date = datetime.now()
    date_str = date.strftime("%d %b %Y")  # Format: "16 Dec 2025"
    
    try:
        with open(CSV_PATH, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Date'].strip() == date_str:
                    return dict(row)
    except FileNotFoundError:
        print(f"\nPrayer times file not found: {CSV_PATH}\n")
    
    return None

def format_prayer_times(prayer_times_data):
    """Format prayer times into a table."""
    
    def format_time(value):
        """Validate and format time string."""
        if not value or not value.strip():
            return "––––––––––"
        
        return value.strip()
    
    if not prayer_times_data:
        prayer_times_data = {}
    
    prayers = [
        ("Fajr", "Fajr_Adhan", "Fajr_Iqamah"),
        ("Sunrise", "Sunrise", None),
        ("Dhuhr", "Dhuhr_Adhan", "Dhuhr_Iqamah"),
        ("Asr", "Asr_Adhan", "Asr_Iqamah"),
        ("Maghrib", "Maghrib_Adhan", "Maghrib_Iqamah"),
        ("Isha", "Isha_Adhan", "Isha_Iqamah"),
        ("Jummah", "Jummah_Adhan", "Jummah_Iqamah"),
    ]
    
    prayer_times = [
        (name, 
        format_time(prayer_times_data.get(adhan, '')), 
        format_time(prayer_times_data.get(iqamah, '')) if iqamah else "––––––––––")
        for name, adhan, iqamah in prayers
    ]
    
    return prayer_times

def render_prayer_table(screen, prayer_table, scale_x, scale_y):
    """Render the prayer times table."""
    
    font_size = int(63 * scale_y)
    table_font = pygame.font.Font(FONT_PATH, font_size)
    
    table_start_x, table_start_y = int(46 * scale_x), int(252 * scale_y)
    vertical_spacing = int(font_size * 1.2)
    col_widths = [int(170 * scale_x), int(275 * scale_x), int(186 * scale_x)]
    
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
        screen.blit(table_font.render(prayer_name, True, RED_COLOR), (col_positions[0], y))  # Left-aligned
        render_centered(adhan, RED_COLOR, 1, y)
        render_centered(iqamah, RED_COLOR, 2, y)