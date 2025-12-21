# countdown.py

from datetime import datetime, timedelta
from config import BLACK_COLOR, RED_COLOR, FOREST_GREEN_COLOR
from utils import get_prayer_times, parse_time

def get_next_prayer(now):
    """Find the next prayer after current time."""
    
    prayer_times = get_prayer_times()
    
    if not prayer_times:
        return None, None
    
    prayers = [
        ("Fajr", "Fajr"),
        ("Dhuhr", "Dhuhr"),
        ("Asr", "Asr"),
        ("Maghrib", "Maghrib"),
        ("Isha", "Isha"),
    ]
    
    for prayer_name, adhan_key in prayers:
        adhan_time_str = prayer_times.get(adhan_key, "")
        adhan_time = parse_time(adhan_time_str)
        
        if adhan_time:
            adhan_datetime = datetime.combine(now.date(), adhan_time)
            
            # Check if this prayer is still today (in the future)
            if adhan_datetime > now:
                return prayer_name, adhan_datetime
    
    # If all prayers for today have passed, return Fajr of next day
    adhan_time_str = prayer_times.get("Fajr", "")
    adhan_time = parse_time(adhan_time_str)
    if adhan_time:
        next_prayer_time = datetime.combine(now.date(), adhan_time) + timedelta(days=1)
        return "Fajr", next_prayer_time
    
    return None, None

def render_countdown(screen, scale_x, scale_y, title_font, time_font):
    """Render the countdown to next prayer."""
    
    next_prayer, next_prayer_time = get_next_prayer(datetime.now())
    
    if next_prayer and next_prayer_time:
        # Calculate time difference
        time_diff = next_prayer_time - datetime.now() + timedelta(seconds=1)
        total_seconds = int(time_diff.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        # Render header and countdown
        countdown_header_surface = title_font.render(f"Time Until {next_prayer}:", True, RED_COLOR)
        countdown_surface = time_font.render(f"{hours:02d}:{minutes:02d}:{seconds:02d}", True, BLACK_COLOR)
        
        countdown_header_rect = countdown_header_surface.get_rect(center=(int(1215 * scale_x), int(670 * scale_y)))
        countdown_rect = countdown_surface.get_rect(center=(int(1217 * scale_x), int(801 * scale_y)))
        
        screen.blit(countdown_header_surface, countdown_header_rect)
        screen.blit(countdown_surface, countdown_rect)