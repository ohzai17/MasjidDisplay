# countdown.py

import math
from datetime import datetime, timedelta
from audio import generate_beep
from utils import render_text, get_text_colors
from table import load_prayer_times, format_table

def get_next_event(now, formatted_prayer_times):
    """Return the next prayer event and its time."""
    
    # List of prayers for the day; replace Dhuhr with Jummah on Fridays
    prayers = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
    if now.weekday() == 4:
        prayers = ["Fajr", "Sunrise", "Jummah", "Asr", "Maghrib", "Isha"]
    
    PLACEHOLDER = "––––––––––"
    
    # Map prayer names to their formatted times for quick lookup
    prayer_map = {name: (name, adhan, iqamah) for name, adhan, iqamah in formatted_prayer_times}
    
    for prayer in prayers:
        if prayer not in prayer_map:
            continue
        _, adhan, iqamah = prayer_map[prayer]
        if adhan == PLACEHOLDER:
            continue
        
        # Determine 'In Progress' durations for each prayer
        if prayer.upper() == "JUMMAH":
            duration = 30
        elif prayer.upper() in ["FAJR", "DHUHR", "ASR", "MAGHRIB", "ISHA"]:
            duration = 15
        else:
            duration = 0
        
        try:
            adhan_dt = datetime.strptime(adhan, "%I:%M %p").replace(
                year=now.year, month=now.month, day=now.day
            )
        except Exception:
            continue
        
        # If current time is before Adhan, return countdown to Adhan
        if now < adhan_dt:
            return ("Adhan", prayer, adhan_dt, duration)
        
        # If Iqamah time exists and is valid, check for Iqamah event or 'In Progress'
        if iqamah != PLACEHOLDER:
            try:
                iqamah_dt = datetime.strptime(iqamah, "%I:%M %p").replace(
                    year=now.year, month=now.month, day=now.day
                )
            except Exception:
                continue
            if now < iqamah_dt:
                return ("Iqamah", prayer, iqamah_dt, duration)
            # If within duration after Iqamah, prayer is 'In Progress'
            elif 0 < duration and iqamah_dt <= now < iqamah_dt + timedelta(minutes=duration):
                return ("In Progress", prayer, iqamah_dt + timedelta(minutes=duration), duration)
        
        # If within duration after Adhan, prayer is 'In Progress'
        if 0 < duration and adhan_dt <= now < adhan_dt + timedelta(minutes=duration):
            return ("In Progress", prayer, adhan_dt + timedelta(minutes=duration), duration)
    
    # If all today's prayers have passed, show next day's Fajr
    tomorrow = now + timedelta(days=1)
    prayer_times = load_prayer_times()
    formatted_prayer_times = format_table(prayer_times)
    prayer_map = {name: (name, adhan, iqamah) for name, adhan, iqamah in formatted_prayer_times}
    if "Fajr" in prayer_map:
        _, adhan, _ = prayer_map["Fajr"]
        if adhan != PLACEHOLDER:
            try:
                adhan_dt = datetime.strptime(adhan, "%I:%M %p").replace(
                    year=tomorrow.year, month=tomorrow.month, day=tomorrow.day
                )
            except Exception:
                return (None, None, None, None)
            duration = 15 # Fajr duration
            return ("Adhan", "Fajr", adhan_dt, duration)
    return (None, None, None, None)

# Track last event 
_last_event = None

def render_countdown(screen, scale_x, scale_y, title_font, time_font):
    """Render countdown to next prayer event."""
    
    global _last_event
    
    primary, secondary, tertiary = get_text_colors()
    
    from test import set_datetime  # Temporary: Use test mode datetime
    now = set_datetime()
    
    # Get formatted prayer times for today
    prayer_times = load_prayer_times()
    formatted_prayer_times = format_table(prayer_times)
    event, prayer, event_time, _ = get_next_event(now, formatted_prayer_times)
    
    # Play a beep when moving to a new event (Adhan or Iqamah)
    current_event = (event, prayer, event_time) if event else None
    if _last_event != current_event:
        if _last_event and _last_event[0] in ("Adhan", "Iqamah"): # Only beep on Adhan and Iqamah
            generate_beep().play()
    # _last_event = current_event # Commented for testing, uncomment in production
    
    if event and prayer and event_time:
        # If prayer is in progress, show status
        if event == "In Progress":
            header = f"{prayer}"
            countdown = "In Progress"
        else:
            # Calculate countdown to next event
            delta = event_time - now
            hours, remainder = divmod(max(0, math.ceil(delta.total_seconds())), 3600)
            minutes, seconds = divmod(remainder, 60)
            countdown = f"{hours:02}:{minutes:02}:{seconds:02}"
            
            # Set header text based on event and prayer type
            if prayer == "Sunrise":
                header = "Time Until Sunrise"
            else:
                header = f"Time Until {prayer}" if event == "Adhan" else "Time Until Iqamah"
        
        render_text(
            screen, header, title_font, primary,
            (int(1215 * scale_x), int(670 * scale_y)),
            align="center", shadow_color=tertiary
        )
        
        render_text(
            screen, countdown, time_font, secondary,
            (int(1217 * scale_x), int(801 * scale_y)),
            align="center", shadow_color=tertiary
        )