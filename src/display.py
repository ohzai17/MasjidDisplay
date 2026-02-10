# display.py

from datetime import datetime, timedelta
from hijridate import Gregorian
from config import load_settings, HIJRI_MONTH_NAMES
from utils import render_text, get_text_colors
from table import load_prayer_times

def render_main(screen, scale_x, scale_y, time_font, title_font, detail_font):
    """Render main display."""
    
    settings = load_settings()
    
    DISPLAY = settings['DISPLAY']
    NAME = DISPLAY['NAME']
    ADDRESS = DISPLAY['ADDRESS']
    
    DATA = settings['DATA']
    HIJRI_DATE_ADJUSTMENT = DATA['LOCATION']['HIJRI_DATE_ADJUSTMENT']
    
    from test import set_datetime # Temporary: Use test mode datetime
    now = set_datetime()
    
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
    
    primary, secondary, tertiary = get_text_colors()
    
    # Render name
    render_text(
        screen, NAME, title_font, primary,
        (int(1218 * scale_x), int(86 * scale_y)), 
        align="center", shadow_color=tertiary
    )
    
    # Render address
    render_text(
        screen, ADDRESS, detail_font, secondary,
        (int(1218 * scale_x), int(159 * scale_y)),
        align="center", shadow_color=tertiary
    )
    
    # Render time
    render_text(
        screen, time_str, time_font, primary,
        (int(363 * scale_x), int(174 * scale_y)), 
        align="center", shadow_color=tertiary
    )
    
    # Render dates
    render_text(
        screen, dates, detail_font, secondary,
        (int(363 * scale_x), int(68 * scale_y)),
        align="center", shadow_color=tertiary
    )