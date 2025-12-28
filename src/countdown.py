# countdown.py

from datetime import datetime, timedelta
from config import DATA
from utils import (
    get_prayer_times, apply_manual_override, apply_adhan_adjustment,
    format_time, parse_time, get_countdown_time, get_prayer_in_progress,
    render_text, get_text_colors
)
from test import set_datetime # Temporary: Testing function

def get_next_prayer(now):
    """Find the next prayer after current time."""
    
    prayer_times = get_prayer_times()
    
    if not prayer_times:
        return None, None, None, False
    
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
        adhan_time_str = apply_adhan_adjustment(prayer_name, adhan_time_str)
        
        # No Iqamah countdown for Sunrise
        if prayer_name == "Sunrise":
            adhan_time = parse_time(adhan_time_str)
            if adhan_time:
                adhan_datetime = datetime.combine(now.date(), adhan_time)
                if adhan_datetime > now:
                    return prayer_name, adhan_datetime, False, False
            continue
        
        # On Friday, replace Dhuhr with Jummah
        if prayer_name == "Dhuhr" and now.weekday() == 4:
            jummah_adhan_str = DATA['JUMMAH'].get('ADHAN_TIME', '').strip()
            if jummah_adhan_str:
                # Check if Jummah is in progress
                jummah_in_progress, jummah_end_time = get_prayer_in_progress("Jummah", jummah_adhan_str, now)
                if jummah_in_progress:
                    return "Jummah", jummah_end_time, True, True
                
                # Check countdown to Jummah
                countdown_time, is_iqamah = get_countdown_time("Jummah", jummah_adhan_str, now)
                if countdown_time:
                    return "Jummah", countdown_time, is_iqamah, False
            continue
        
        # Regular prayers
        in_progress, prayer_end_time = get_prayer_in_progress(prayer_name, adhan_time_str, now)
        if in_progress:
            return prayer_name, prayer_end_time, True, True
        
        countdown_time, is_iqamah = get_countdown_time(prayer_name, adhan_time_str, now)
        if countdown_time:
            return prayer_name, countdown_time, is_iqamah, False
    
    # Countdown to next day's Fajr adhan if all today's prayers have passed
    api_time = prayer_times.get("Fajr", "")
    adhan_time_str = format_time(apply_manual_override("Fajr", api_time))
    adhan_time_str = apply_adhan_adjustment("Fajr", adhan_time_str)
    adhan_time = parse_time(adhan_time_str)
    if adhan_time:
        next_prayer_adhan = datetime.combine(now.date(), adhan_time) + timedelta(days=1)
        return "Fajr", next_prayer_adhan, False, False
    
    return None, None, None, False

def render_countdown(screen, scale_x, scale_y, title_font, time_font, current_seconds, prayer_times_seconds):
    """Render the countdown."""
    
    next_prayer, next_prayer_time, is_iqamah, in_progress = get_next_prayer(set_datetime())
    
    primary_color, secondary_color, tertiary_color = get_text_colors(current_seconds, prayer_times_seconds)
    
    if next_prayer and next_prayer_time:
        # Format header text
        if in_progress:
            header_text = f"{next_prayer}"
            countdown_text = "In Progress"
        else:
            # Calculate time difference
            time_diff = next_prayer_time - set_datetime()
            total_seconds = int(time_diff.total_seconds()) + 1
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            countdown_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            if next_prayer == "Sunrise":
                header_text = "Time Until Sunrise:"
            elif next_prayer == "Jummah":
                header_text = "Time Until Khutbah:" if is_iqamah else "Time Until Jummah:"
            else:
                header_text = "Time Until Iqamah:" if is_iqamah else f"Time Until {next_prayer}:"
        
        render_text(
            screen, header_text, title_font, primary_color,
            (int(1215 * scale_x), int(670 * scale_y)),
            align="center"
        )
        
        render_text(
            screen, countdown_text, time_font, tertiary_color,
            (int(1217 * scale_x), int(801 * scale_y)),
            align="center", outline_color=secondary_color
        )