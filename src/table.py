# table.py

import csv
import pygame
from datetime import datetime, timedelta
from config import CSV_PATH, FONT_PATH, DATA, BLACK_COLOR, RED_COLOR, FOREST_GREEN_COLOR

def get_prayer_times():
    """Load prayer times from CSV file."""
    
    date = datetime.now()
    date_str = date.strftime("%d %b %Y")  # Format: "16 Dec 2025"
    
    try:
        with open(CSV_PATH, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Date'].strip() == date_str:
                    return dict(row)
    except FileNotFoundError:
        print(f"\nCSV file not found: {CSV_PATH}\n")
    
    return None

def apply_manual_override(prayer_name: str, api_time: str):
    """Return manual override if available, otherwise return API time."""
    
    if not api_time or not api_time.strip():
        return ""
    
    adhan_times = DATA['ADHAN_TIMES']
    manual_time = adhan_times.get(prayer_name.upper(), "").strip()
    
    return manual_time if manual_time else api_time

def format_prayer_table(prayer_times):
    """Format prayer times into a table."""
    
    def format_time(value):
        """Validate and format time string."""
        if not value or not value.strip():
            return "––––––––––"
        
        return value.strip()
    
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
    
    date_str = prayer_times.get('Date', '')
    iqamah_offsets = DATA['IQAMAH_OFFSETS']
    
    for prayer_name, csv_key in prayers:
        
        api_time = prayer_data.get(csv_key, '')
        adhan_time = format_time(apply_manual_override(prayer_name, api_time))
        iqamah_time = PLACEHOLDER
        
        # Calculate Iqamah time
        if adhan_time != PLACEHOLDER:
            try:
                adhan_datetime = datetime.strptime(f"{date_str} {adhan_time}", "%d %b %Y %I:%M %p")
                offset_minutes = int(iqamah_offsets[prayer_name.upper()])
                iqamah_datetime = adhan_datetime + timedelta(minutes=offset_minutes)
                iqamah_time = iqamah_datetime.strftime("%I:%M %p")
            except (ValueError, KeyError):
                pass
        else:
            iqamah_time = PLACEHOLDER
        
        formatted_prayer_times.append((prayer_name, adhan_time, iqamah_time))
    
    # Handle Jummah
    jummah = DATA['JUMMAH']
    jummah_adhan = jummah.get('ADHAN_TIME', '').strip()
    jummah_iqamah_offset = jummah.get('IQAMAH_OFFSET')
    
    if jummah_adhan:
        try:
            jummah_datetime = datetime.strptime(f"{date_str} {jummah_adhan}", "%d %b %Y %I:%M %p")
            jummah_adhan_time = jummah_datetime.strftime("%I:%M %p")
            jummah_iqamah_datetime = jummah_datetime + timedelta(minutes=jummah_iqamah_offset)
            jummah_iqamah_time = jummah_iqamah_datetime.strftime("%I:%M %p")
            
            formatted_prayer_times.append(("Jummah", jummah_adhan_time, jummah_iqamah_time))
        except (ValueError, KeyError):
            formatted_prayer_times.append(("Jummah", PLACEHOLDER, PLACEHOLDER))
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
    
    from countdown import get_next_prayer
    
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