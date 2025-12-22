# countdown.py

from datetime import datetime, timedelta
from config import RED_COLOR, FOREST_GREEN_COLOR
from utils import get_prayer_times, apply_manual_override, format_time, parse_time, calculate_iqamah

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
        adhan_time = parse_time(adhan_time_str)
        
        if adhan_time:
            adhan_datetime = datetime.combine(now.date(), adhan_time)
            
            # No Iqamah countdown for Sunrise
            if prayer_name == "Sunrise":
                if adhan_datetime > now:
                    return prayer_name, adhan_datetime, False
                continue
            
            # Check if Adhan is upcoming or passed
            if adhan_datetime > now:
                # Adhan is next, count down to Adhan
                return prayer_name, adhan_datetime, False
            else:
                # Adhan has passed, check if Iqamah hasn't passed yet
                iqamah_time_str = calculate_iqamah(adhan_time_str, prayer_name)
                if iqamah_time_str:
                    iqamah_time = parse_time(iqamah_time_str)
                    if iqamah_time:
                        iqamah_datetime = datetime.combine(now.date(), iqamah_time)
                        # If Iqamah hasn't happened yet, count down to it
                        if iqamah_datetime > now:
                            return prayer_name, iqamah_datetime, True
                        
                        # If Iqamah has passed, the loop continues to the next prayer
    
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
            header_text = f"Time Until Sunrise"
        elif is_iqamah:
            header_text = f"Time Until Iqamah"
        else:
            header_text = f"Time Until {next_prayer}"
        
        # Render header and countdown
        countdown_header_surface = title_font.render(header_text, True, FOREST_GREEN_COLOR)
        countdown_surface = time_font.render(f"{hours:02d}:{minutes:02d}:{seconds:02d}", True, RED_COLOR)
        
        countdown_header_rect = countdown_header_surface.get_rect(center=(int(1215 * scale_x), int(670 * scale_y)))
        countdown_rect = countdown_surface.get_rect(center=(int(1217 * scale_x), int(801 * scale_y)))
        
        screen.blit(countdown_header_surface, countdown_header_rect)
        screen.blit(countdown_surface, countdown_rect)