# display.py

from hijridate import Gregorian
from config import NAME, ADDRESS, HIJRI_MONTH_NAMES
from utils import render_text, get_text_colors

def render_main(screen, scale_x, scale_y, time_font, title_font, detail_font):
    """Render main display."""
    
    from test import set_datetime # Temporary: Use test mode datetime
    now = set_datetime()
    
    # Time and date formatting
    time_str = now.strftime("%I:%M:%S %p")
    date_str = now.strftime("%d %B %Y")
    
    # Hijri date formatting
    hijri_date = Gregorian(now.year, now.month, now.day).to_hijri()
    hijri_month_name = HIJRI_MONTH_NAMES[hijri_date.month]
    hijri_str = f"{hijri_date.day:02d} {hijri_month_name} {hijri_date.year}"
    
    dates = date_str + " · " + hijri_str # Combine Gregorian and Hijri dates
    
    primary, secondary, _ = get_text_colors()
    
    # Render name
    render_text(
        screen, NAME, title_font, primary,
        (int(1218 * scale_x), int(86 * scale_y)), 
        align="center"
    )
    
    # Render address
    render_text(
        screen, ADDRESS, detail_font, secondary,
        (int(1218 * scale_x), int(159 * scale_y)),
        align="center"
    )
    
    # Render time
    render_text(
        screen, time_str, time_font, primary,
        (int(363 * scale_x), int(174 * scale_y)), 
        align="center"
    )
    
    # Render dates
    render_text(
        screen, dates, detail_font, secondary,
        (int(363 * scale_x), int(68 * scale_y)),
        align="center"
    )