# table.py

from config import DATA
from countdown import get_next_prayer
from utils import (
    apply_manual_override, format_time, calculate_iqamah, render_text,
    get_text_colors
)
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

def render_prayer_table(screen, prayer_table, scale_x, scale_y, table_font, current_seconds, prayer_times_seconds):
    """Render the prayer times table."""
    
    table_start_x, table_start_y = int(47 * scale_x), int(298 * scale_y)
    vertical_spacing = int(table_font.get_height() * 1.0)
    col_widths = [int(170 * scale_x), int(275 * scale_x), int(186 * scale_x)]
    
    next_prayer, _, _, _ = get_next_prayer(set_datetime()) # Temporary: Use test mode datetime
    
    # Calculate starting x-positions for each column
    col_positions = [table_start_x,
            table_start_x + col_widths[0],
            table_start_x + col_widths[0] + col_widths[1]]
    
    primary_color, secondary_color, tertiary_color = get_text_colors(current_seconds, prayer_times_seconds)
    
    # Render header
    for col_idx, header_text in enumerate(["", "Adhan", "Iqamah"]):
        x = col_positions[col_idx] + col_widths[col_idx] // 2
        y = table_start_y
        
        render_text(
            screen, header_text, table_font, primary_color,
            (x, y), align="center"
        )
    
    # Render prayer rows
    for i, (prayer_name, adhan, iqamah) in enumerate(prayer_table):
        y = table_start_y + ((i + 1) * vertical_spacing)
        
        if prayer_name == next_prayer:
            color = tertiary_color
            outline_color = secondary_color
        else:
            color = secondary_color
            outline_color = None
        
        # Render prayer name
        render_text(
            screen, prayer_name, table_font, primary_color,
            (col_positions[0], y), align="left"
        )
        
        # Render Adhan
        x_adhan = col_positions[1] + col_widths[1] // 2
        render_text(
            screen, adhan, table_font, color,
            (x_adhan, y), align="center",
            outline_color=outline_color
        )
        
        # Render Iqamah
        x_iqamah = col_positions[2] + col_widths[2] // 2
        render_text(
            screen, iqamah, table_font, color,
            (x_iqamah, y), align="center",
            outline_color=outline_color
        )