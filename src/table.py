# table.py

import csv
from datetime import datetime, timedelta
from config import CSV, DATA, BLACK
from utils import render_text, get_text_colors

def load_prayer_times():
    """Load today's prayer times from CSV."""
    
    from test import set_datetime # Temporary: Use test mode datetime
    today_str = set_datetime().strftime('%d %b %Y')
    
    try:
        with open(CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Date'].strip() == today_str:
                    return {k: v for k, v in row.items() if k != 'Date'}
    except FileNotFoundError:
        pass
    return {}

def format_table(prayer_times):
    """Format prayer times into a table."""
    
    prayers = [
        "Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha", "Jummah"
    ]
    
    PLACEHOLDER = "––––––––––"
    formatted_prayer_times = []
    
    # If no CSV data for today, show placeholders for all prayers
    if not prayer_times:
        for prayer_name in prayers:
            formatted_prayer_times.append((prayer_name, PLACEHOLDER, PLACEHOLDER))
        return formatted_prayer_times
    
    for prayer_name in prayers:
        # Get the base time from CSV
        base_time = prayer_times.get(prayer_name, "")
        
        # Manual override from config
        manual_time = DATA["PRAYERS"].get(prayer_name.upper(), {}).get("ADHAN_TIME", "").strip()
        
        # No CSV column for Jummah
        if prayer_name == "Jummah":
            adhan_time = manual_time
        else:
            adhan_time = manual_time if manual_time else base_time
        
        # Format adhan time
        adhan_time = adhan_time.strip() if adhan_time and adhan_time.strip() else PLACEHOLDER
        
        # Apply adjustment
        adjustment = DATA["PRAYERS"].get(prayer_name.upper(), {}).get("ADJUSTMENT", 0)
        if adhan_time != PLACEHOLDER:
            try:
                adhan_dt = datetime.strptime(adhan_time, "%I:%M %p")
                adhan_dt += timedelta(minutes=adjustment)
                adhan_time = adhan_dt.strftime("%I:%M %p")
            except Exception:
                pass
        
        # Calculate Iqamah time
        iqamah_time = PLACEHOLDER
        if adhan_time != PLACEHOLDER:
            iqamah_offset = DATA["PRAYERS"].get(prayer_name.upper(), {}).get("IQAMAH_OFFSET")
            try:
                adhan_dt = datetime.strptime(adhan_time, "%I:%M %p")
                iqamah_dt = adhan_dt + timedelta(minutes=iqamah_offset)
                iqamah_time = iqamah_dt.strftime("%I:%M %p")
            except Exception:
                pass
        
        formatted_prayer_times.append((prayer_name, adhan_time, iqamah_time))
    
    return formatted_prayer_times

def render_table(screen, scale_x, scale_y, table_font):
    """Render the prayer times table."""
    
    primary, secondary, tertiary = get_text_colors()
    
    prayer_times = load_prayer_times()
    
    table_start_x, table_start_y = int(47 * scale_x), int(298 * scale_y)
    vertical_spacing = int(table_font.get_height() * 1.0)
    col_widths = [int(170 * scale_x), int(275 * scale_x), int(186 * scale_x)]
    
    # Calculate starting x-positions for each column
    col_positions = [table_start_x,
            table_start_x + col_widths[0],
            table_start_x + col_widths[0] + col_widths[1]]
    
    # Render header
    for col_idx, header_text in enumerate(["", "Adhan", "Iqamah"]):
        x = col_positions[col_idx] + col_widths[col_idx] // 2
        y = table_start_y
        
        render_text(
            screen, header_text, table_font, primary,
            (x, y), align="center"
        )
    
    # Render prayer rows
    for i, (prayer_name, adhan, iqamah) in enumerate(format_table(prayer_times)):
        y = table_start_y + ((i + 1) * vertical_spacing)
        
        # Render prayer name
        render_text(
            screen, prayer_name, table_font, primary,
            (col_positions[0], y), align="left"
        )
        
        # Render Adhan
        x_adhan = col_positions[1] + col_widths[1] // 2
        render_text(
            screen, adhan, table_font, secondary,
            (x_adhan, y), align="center"
        )
        
        # Render Iqamah
        x_iqamah = col_positions[2] + col_widths[2] // 2
        render_text(
            screen, iqamah, table_font, secondary,
            (x_iqamah, y), align="center"
        )