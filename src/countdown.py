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
        
        try:
            adhan_dt = datetime.strptime(adhan, "%I:%M %p").replace(
                year=now.year, month=now.month, day=now.day
            )
        except Exception:
            continue
        
        # If current time is before Adhan, return countdown to Adhan
        if now < adhan_dt:
            return ("Adhan", prayer, adhan_dt)
        
        # If Iqamah time exists and is valid, check for Iqamah event
        if iqamah != PLACEHOLDER:
            try:
                iqamah_dt = datetime.strptime(iqamah, "%I:%M %p").replace(
                    year=now.year, month=now.month, day=now.day
                )
            except Exception:
                continue
            if now < iqamah_dt:
                return ("Iqamah", prayer, iqamah_dt)
    
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
                return (None, None, None)
            return ("Adhan", "Fajr", adhan_dt)
    return (None, None, None)

# Track last event
_last_event = None

def render_countdown(screen, scale_x, scale_y, clock_font, title_font, countdown_font, show_announcements=False):
    """Render countdown to next prayer event."""
    
    primary, secondary, tertiary = get_text_colors()
    
    now = datetime.now()
    
    # Get formatted prayer times for today
    prayer_times = load_prayer_times()
    formatted_prayer_times = format_table(prayer_times)
    event, prayer, event_time = get_next_event(now, formatted_prayer_times)
    
    global _last_event
    
    # Play a beep on Adhan and Iqamah event changes
    current_event = (event, prayer, event_time) if event else None
    if _last_event != current_event:
        if _last_event and _last_event[0] in ("Adhan", "Iqamah"):
            # generate_beep().play()
            print("Beep!")
    _last_event = current_event
    
    if event and prayer and event_time:
        
        # Calculate countdown to next event
        delta = event_time - now
        hours, remainder = divmod(max(0, math.ceil(delta.total_seconds())), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Define unit labels
        if hours >= 1:
            value = hours
            label = "Hour" if value == 1 else "Hours"
        elif minutes >= 1:
            value = minutes
            label = "Minute" if value == 1 else "Minutes"
        else:
            value = seconds
            label = "Second" if value == 1 else "Seconds"
        
        countdown = f"{value:02d}"
        
        # Set header text based on event and prayer type
        if prayer == "Sunrise":
            header = "Time Until Sunrise"
        else:
            header = f"Time Until {prayer}:" if event == "Adhan" else "Time Until Iqamah:"
        
        if show_announcements:
            render_text(
                screen, header, title_font, primary,
                (int(1204 * scale_x), int(558 * scale_y)),
                align="center", shadow_color=tertiary
            )
            
            render_text(
                screen, countdown, clock_font, secondary,
                (int(1206 * scale_x), int(687 * scale_y)),
                align="center", shadow_color=tertiary
            )
            
            render_text(
                screen, label, title_font, primary,
                (int(1205 * scale_x), int(814 * scale_y)),
                align="center", shadow_color=tertiary
            )
        
        else:
            render_text(
                screen, header, title_font, primary,
                (int(1204 * scale_x), int(357 * scale_y)),
                align="center", shadow_color=tertiary
            )
            
            render_text(
                screen, countdown, countdown_font, secondary,
                (int(1206 * scale_x), int(575 * scale_y)),
                align="center", shadow_color=tertiary
            )
            
            render_text(
                screen, label, title_font, primary,
                (int(1205 * scale_x), int(765 * scale_y)),
                align="center", shadow_color=tertiary
            )