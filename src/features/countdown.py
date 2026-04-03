# countdown.py

import pygame
from src.config import BEEP
from datetime import datetime
from src.utils import (
    load_prayer_times, get_prayer_times, get_next_event, get_text_colors, render_text)

# Track if beep has been played for current countdown
beep_played = False
last_event_time = None

def render_countdown(screen, scale_x, scale_y, clock_font, title_font, countdown_font, show_announcements):
    """Render countdown to next prayer event."""
    
    global beep_played, last_event_time
    
    primary, secondary, tertiary = get_text_colors()
    
    now = datetime.now()
    
    # Get formatted prayer times for today
    prayer_times = load_prayer_times()
    formatted_prayer_times = get_prayer_times(prayer_times)
    event, prayer, event_time = get_next_event(now, formatted_prayer_times)
    
    if event and prayer and event_time:
        
        # Reset beep flag if event time has changed
        if event_time != last_event_time:
            beep_played = False
            last_event_time = event_time
        
        # Calculate countdown to next event
        delta = event_time - now
        total_seconds = max(0, int(delta.total_seconds()))
        
        # Play beep when timer reaches zero
        if total_seconds <= 0 and not beep_played:
            pygame.mixer.Sound(BEEP).play()
            beep_played = True
        
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