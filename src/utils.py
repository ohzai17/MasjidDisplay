# utils.py

import csv
import pygame
from datetime import datetime, timedelta
from config import (
    CSV_PATH, DATA, BLACK_COLOR, WHITE_COLOR, NAVY_BLUE_COLOR, PEACH_COLOR
)

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

def apply_adhan_adjustment(prayer_name: str, time_str: str):
    """Return adhan time with adjustment (in minutes) if set in settings."""
    
    if not time_str or not time_str.strip():
        return ""
    
    adjustments = DATA.get('ADHAN_ADJUSTMENTS', {})
    adjustment = adjustments.get(prayer_name.upper(), 0)
    
    try:
        adhan_datetime = datetime.strptime(time_str.strip(), "%I:%M %p")
        adhan_datetime += timedelta(minutes=adjustment)
        return adhan_datetime.strftime("%I:%M %p")
    except ValueError:
        return time_str

def format_time(time_str):
    """Validate and format time string."""
    
    if not time_str or not time_str.strip():
        return "––––––––––"
    return time_str.strip()

def parse_time(time_str):
    """Convert time string to datetime object."""
    
    try:
        return datetime.strptime(time_str.strip(), "%I:%M %p").time()
    except ValueError:
        return None
    
def get_seconds(prayer_times):
    """Get prayer times in seconds since midnight."""
    
    if not prayer_times:
        return None
    def to_sec(t_str):
        t = datetime.strptime(t_str.strip(), "%I:%M %p")
        return t.hour * 3600 + t.minute * 60
    return {k: to_sec(v) for k, v in prayer_times.items() if k != 'Date'}

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

def render_text(
    surface, text, font, color, pos,
    align="center",
    scale_x = 1.0, scale_y = 1.0,
    outline_color = None, outline_width = 2,
    shadow_color = None, shadow_offset = (2, 2)
):
    """Render text."""
    
    # Render text surface
    text_surface = font.render(text, True, color)
    size = (int(text_surface.get_width() * scale_x), int(text_surface.get_height() * scale_y))
    
    # Custom scaling
    if scale_x != 1.0 or scale_y != 1.0:
        text_surface = pygame.transform.smoothscale(text_surface, size)
    
    # Outline
    if outline_color and outline_width > 0:
        base = font.render(text, True, outline_color)
        if scale_x != 1.0 or scale_y != 1.0:
            base = pygame.transform.smoothscale(base, size)
        outline_surface = pygame.Surface((text_surface.get_width() + 2*outline_width, text_surface.get_height() + 2*outline_width), pygame.SRCALPHA)
        for dx in range(-outline_width, outline_width+1):
            for dy in range(-outline_width, outline_width+1):
                if dx != 0 or dy != 0:
                    outline_surface.blit(base, (dx+outline_width, dy+outline_width))
        outline_surface.blit(text_surface, (outline_width, outline_width))
        text_surface = outline_surface
    
    # Shadow
    if shadow_color:
        shadow_surface = font.render(text, True, shadow_color)
        if scale_x != 1.0 or scale_y != 1.0:
            shadow_surface = pygame.transform.smoothscale(shadow_surface, size)
        shadow_pos = (shadow_offset[0], shadow_offset[1])
        shadow_layer = pygame.Surface((text_surface.get_width() + abs(shadow_pos[0]), text_surface.get_height() + abs(shadow_pos[1])), pygame.SRCALPHA)
        shadow_layer.blit(shadow_surface, shadow_pos)
        shadow_layer.blit(text_surface, (0, 0))
        text_surface = shadow_layer
    
    # Alignment
    rect = text_surface.get_rect()
    x, y = pos
    if align == "center":
        rect.center = (x, y)
    elif align == "left":
        rect.midleft = (x, y)
    elif align == "right":
        rect.midright = (x, y)
    else:
        rect.topleft = (x, y)
    
    surface.blit(text_surface, rect)
    
    return rect

def get_text_colors(current_seconds, prayer_times_seconds):
    """Adjust text colors."""
    
    if not prayer_times_seconds:
        return BLACK_COLOR, BLACK_COLOR, BLACK_COLOR
    
    # Calculate window boundaries (in seconds since midnight)
    day_start = (prayer_times_seconds["Sunrise"] - 2700) % 86400   # 45 min before Sunrise
    day_end = (prayer_times_seconds["Maghrib"] - 2700) % 86400  # 45 min before Maghrib
    
    # Determine if current time is in the daytime window
    if day_start < day_end:
        is_daytime = day_start <= current_seconds < day_end
    else:
        # Rare case where window crosses midnight
        is_daytime = current_seconds >= day_start or current_seconds < day_end
    
    if is_daytime:
        return NAVY_BLUE_COLOR, BLACK_COLOR, WHITE_COLOR  # Day colors
    else:
        return PEACH_COLOR, WHITE_COLOR, BLACK_COLOR  # Night colors