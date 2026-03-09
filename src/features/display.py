# display.py

from hijridate import Gregorian
from src.config import HIJRI_MONTH_NAMES
from datetime import datetime, timedelta
from src.utils import load_settings, load_prayer_times, get_text_colors, render_text

def render_display(screen, scale_x, scale_y, clock_font, title_font, detail_font, theme_index):
    """Render main display."""
    
    settings = load_settings()
    
    DISPLAY = settings['DISPLAY']
    NAME = DISPLAY['NAME']
    ADDRESS = DISPLAY['ADDRESS']
    
    DATA = settings['DATA']
    HIJRI_DATE_ADJUSTMENT = DATA['LOCATION']['HIJRI_DATE_ADJUSTMENT']
    
    now = datetime.now()
    
    # Time and date formatting
    time_str = now.strftime("%I:%M:%S %p")
    date_str = now.strftime("%d %B %Y")
    
    prayer_times = load_prayer_times()
    
    # Advance Hijri date if past Maghrib
    hijri_date_dt = now
    try:
        maghrib_str = prayer_times.get("Maghrib") if prayer_times else None
        if maghrib_str:
            maghrib_time = datetime.strptime(maghrib_str, "%I:%M %p")
            maghrib_dt = now.replace(
                hour=maghrib_time.hour, minute=maghrib_time.minute
            )
            if now >= maghrib_dt:
                hijri_date_dt += timedelta(days=1)
    except Exception:
        pass
    
    # Apply Hijri date adjustment
    hijri_date_dt += timedelta(days=HIJRI_DATE_ADJUSTMENT)
    
    # Hijri date formatting
    hijri_date = Gregorian(hijri_date_dt.year, hijri_date_dt.month, hijri_date_dt.day).to_hijri()
    hijri_month_name = HIJRI_MONTH_NAMES[hijri_date.month]
    hijri_str = f"{hijri_date.day:02d} {hijri_month_name} {hijri_date.year}"
    
    dates = date_str + " · " + hijri_str # Combine Gregorian and Hijri dates
    
    primary, secondary, tertiary = get_text_colors(theme_index)
    
    # Render name
    render_text(
        screen, NAME, title_font, primary,
        (int(1204 * scale_x), int(86 * scale_y)), 
        align="center", shadow_color=tertiary
    )
    
    # Render address
    render_text(
        screen, ADDRESS, detail_font, secondary,
        (int(1204 * scale_x), int(159 * scale_y)),
        align="center", shadow_color=tertiary
    )
    
    # Render clock
    render_text(
        screen, time_str, clock_font, primary,
        (int(443 * scale_x), int(174 * scale_y)), 
        align="center", shadow_color=tertiary
    )
    
    # Render dates
    render_text(
        screen, dates, detail_font, secondary,
        (int(443 * scale_x), int(68 * scale_y)),
        align="center", shadow_color=tertiary
    )