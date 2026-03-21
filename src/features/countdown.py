# countdown.py

from datetime import datetime
from src.audio import generate_beep
from src.utils import (
    load_prayer_times, get_prayer_times, get_next_event, get_text_colors, render_text)

initial_frame = True
previous_event = None

def render_countdown(screen, scale_x, scale_y, clock_font, title_font, countdown_font, show_announcements):
    """Render countdown to next prayer event."""
    
    global initial_frame, previous_event
    
    primary, secondary, tertiary = get_text_colors()
    
    now = datetime.now()
    
    # Get formatted prayer times for today
    prayer_times = load_prayer_times()
    formatted_prayer_times = get_prayer_times(prayer_times)
    event, prayer, event_time = get_next_event(now, formatted_prayer_times)
    
    current_event = (event, prayer) if event and prayer else (None, None)
    
    # Check if event has changed and trigger beep
    if not initial_frame and current_event != previous_event and current_event != (None, None):
        generate_beep().play()
    
    # Reset initial frame and update previous event
    initial_frame = False
    previous_event = current_event
    
    if event and prayer and event_time:
        
        # Calculate countdown to next event
        delta = event_time - now
        total_seconds = max(0, int(delta.total_seconds())) + 1
        hours, remainder = divmod(total_seconds, 3600)
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
                (int(1204 * scale_x), int(267 * scale_y)),
                align="center", shadow_color=tertiary
            )
            
            render_text(
                screen, countdown, clock_font, secondary,
                (int(1206 * scale_x), int(396 * scale_y)),
                align="center", shadow_color=tertiary
            )
            
            render_text(
                screen, label, title_font, primary,
                (int(1205 * scale_x), int(523 * scale_y)),
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