# countdown.py

from datetime import datetime, timedelta
from config import DATA, RED_COLOR, FOREST_GREEN_COLOR
from utils import get_prayer_times, apply_manual_override, format_time, parse_time, get_countdown_time

from test import set_datetime # Temporary: Testing function

def get_next_prayer(now):
    """Find the next prayer after current time."""
    
    prayer_times = get_prayer_times()
    
    if not prayer_times:
        return None, None, None
    
    prayers = [
        ("Fajr", "Fajr"),
        ("Sunrise", "Sunrise"),
        ("Dhuhr", "Dhuhr"),
        ("Asr", "Asr"),
        ("Maghrib", "Maghrib"),
        ("Isha", "Isha"),
    ]
    
    for prayer_name, adhan_key in prayers:
        api_time = prayer_times.get(adhan_key, "")
        adhan_time_str = format_time(apply_manual_override(prayer_name, api_time))
        
        # No Iqamah countdown for Sunrise
        if prayer_name == "Sunrise":
            adhan_time = parse_time(adhan_time_str)
            if adhan_time:
                adhan_datetime = datetime.combine(now.date(), adhan_time)
                if adhan_datetime > now:
                    return prayer_name, adhan_datetime, False
            continue
        
        # On Friday, replace Dhuhr with Jummah
        if prayer_name == "Dhuhr" and now.weekday() == 4:
            jummah_adhan_str = DATA['JUMMAH'].get('ADHAN_TIME', '').strip()
            if jummah_adhan_str:
                countdown_time, is_iqamah = get_countdown_time("Jummah", jummah_adhan_str, now)
                if countdown_time:
                    return "Jummah", countdown_time, is_iqamah
            continue
        
        # Regular prayers
        countdown_time, is_iqamah = get_countdown_time(prayer_name, adhan_time_str, now)
        if countdown_time:
            return prayer_name, countdown_time, is_iqamah
    
    # Countdown to next day's Fajr adhan if all today's prayers have passed
    api_time = prayer_times.get("Fajr", "")
    adhan_time_str = format_time(apply_manual_override("Fajr", api_time))
    adhan_time = parse_time(adhan_time_str)
    if adhan_time:
        next_prayer_adhan = datetime.combine(now.date(), adhan_time) + timedelta(days=1)
        return "Fajr", next_prayer_adhan, False
    
    return None, None, None

def render_countdown(screen, scale_x, scale_y, title_font, time_font):
    """Render the countdown to next prayer."""
    
    next_prayer, next_prayer_time, is_iqamah = get_next_prayer(set_datetime()) # Temporary: Use test mode datetime
    
    if next_prayer and next_prayer_time:
        # Calculate time difference
        time_diff = next_prayer_time - set_datetime()
        total_seconds = int(time_diff.total_seconds()) + 1 # Add 1 second to avoid negative zero
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        # Format header text
        if next_prayer == "Sunrise":
            header_text = "Time Until Sunrise"
        elif next_prayer == "Jummah":
            header_text = "Time Until Khutbah" if is_iqamah else "Time Until Jummah"
        else:
            header_text = "Time Until Iqamah" if is_iqamah else f"Time Until {next_prayer}"
        
        # Render header and countdown
        countdown_header_surface = title_font.render(header_text, True, FOREST_GREEN_COLOR)
        countdown_surface = time_font.render(f"{hours:02d}:{minutes:02d}:{seconds:02d}", True, RED_COLOR)
        
        countdown_header_rect = countdown_header_surface.get_rect(center=(int(1215 * scale_x), int(670 * scale_y)))
        countdown_rect = countdown_surface.get_rect(center=(int(1217 * scale_x), int(801 * scale_y)))
        
        screen.blit(countdown_header_surface, countdown_header_rect)
        screen.blit(countdown_surface, countdown_rect)