# utils.py

import csv
from datetime import datetime, timedelta
from config import CSV_PATH, DATA

from test import set_datetime  # Temporary: Testing function

def get_prayer_times():
    """Load prayer times from CSV file."""
    
    date = set_datetime() # Temporary: Use test mode datetime
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

def format_time(value):
    """Validate and format time string."""
    
    if not value or not value.strip():
        return "––––––––––"
    return value.strip()

def parse_time(time_str):
    """Convert time string to datetime object."""
    
    try:
        return datetime.strptime(time_str.strip(), "%I:%M %p").time()
    except ValueError:
        return None

def calculate_iqamah(adhan_time_str, prayer_name):
    """Calculate Iqamah time from Adhan time and offset."""
    
    if not adhan_time_str or not adhan_time_str.strip():
        return ""
    
    try:
        adhan_datetime = datetime.strptime(adhan_time_str.strip(), "%I:%M %p")
        
        # Handle Jummah
        if prayer_name.upper() == "JUMMAH":
            jummah = DATA['JUMMAH']
            offset_minutes = int(jummah.get('IQAMAH_OFFSET', 0))
        else:
        # Handle regular prayers
            iqamah_offsets = DATA['IQAMAH_OFFSETS']
            offset_minutes = int(iqamah_offsets[prayer_name.upper()])
        
        iqamah_datetime = adhan_datetime + timedelta(minutes=offset_minutes)
        return iqamah_datetime.strftime("%I:%M %p")
    except (ValueError, KeyError):
        return ""

def get_countdown_time(prayer_name, adhan_time_str, now):
    """Get the countdown (Adhan or Iqamah) for a given prayer."""
    
    adhan_time = parse_time(adhan_time_str)
    if not adhan_time:
        return None, None
    
    adhan_datetime = datetime.combine(now.date(), adhan_time)
    
    # Count down to Adhan if upcoming
    if adhan_datetime > now:
        return adhan_datetime, False
    
    # Adhan has passed, check if Iqamah is upcoming
    iqamah_time_str = calculate_iqamah(adhan_time_str, prayer_name)
    if iqamah_time_str:
        iqamah_time = parse_time(iqamah_time_str)
        if iqamah_time:
            iqamah_datetime = datetime.combine(now.date(), iqamah_time)
            if iqamah_datetime > now:
                return iqamah_datetime, True
    
    # Both have passed
    return None, None

def get_prayer_in_progress(prayer_name, adhan_time_str, now):
    """Check if the Iqamah has passed and the prayer duration has not ended."""
    
    # Calculate Iqamah time first
    iqamah_time_str = calculate_iqamah(adhan_time_str, prayer_name)
    if not iqamah_time_str:
        return False, None
    
    iqamah_time = parse_time(iqamah_time_str)
    if not iqamah_time:
        return False, None
    
    iqamah_datetime = datetime.combine(now.date(), iqamah_time)
    
    # Check if Iqamah has occurred
    if iqamah_datetime > now:
        return False, None
    
    prayer_duration_config = DATA.get('PRAYER_DURATION', {})
    duration_minutes = prayer_duration_config.get(prayer_name.upper(), 15)
    
    prayer_end_time = iqamah_datetime + timedelta(minutes=duration_minutes)
    
    # Check if prayer is still in progress
    if now < prayer_end_time:
        return True, prayer_end_time
    
    return False, None

def render_centered(screen, text, color, col_positions, col_widths, table_font, col, y_pos):
    """Render text centered in the specified column."""
    
    text_surface = table_font.render(text, True, color)
    x = col_positions[col] + (col_widths[col] - text_surface.get_width()) // 2
    screen.blit(text_surface, (x, y_pos))