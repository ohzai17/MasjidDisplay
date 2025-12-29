# display.py

from hijridate import Gregorian
from datetime import timedelta
from config import DATA, HIJRI_MONTH_NAMES, NAME, ADDRESS
from utils import render_text, get_text_colors

def render_main(screen, current_datetime, scale_x, scale_y, time_font, title_font, detail_font, current_seconds, prayer_times_seconds):
    """Render main display."""
    
    # Time and date formatting
    time_str = current_datetime.strftime("%I:%M:%S %p")
    date_str = current_datetime.strftime("%d %B %Y")
    
    # Get the Hijri date
    hijri_date_adjustment = DATA.get('HIJRI_DATE_ADJUSTMENT', 0)
    adjusted_gregorian = current_datetime + timedelta(days=hijri_date_adjustment)
    hijri_date = Gregorian(adjusted_gregorian.year, adjusted_gregorian.month, adjusted_gregorian.day).to_hijri()
    hijri_month_name = HIJRI_MONTH_NAMES[hijri_date.month]
    hijri_str = f"{hijri_date.day:02d} {hijri_month_name} {hijri_date.year}"
    
    dates = date_str + " · " + hijri_str # Combine Gregorian and Hijri dates
    
    primary_color, secondary_color, _ = get_text_colors(current_seconds, prayer_times_seconds)
    
    # Render name
    render_text(
        screen, NAME, title_font, primary_color,
        (int(1218 * scale_x), int(86 * scale_y)), 
        align="center"
    )
    
    # Render address
    render_text(
        screen, ADDRESS, detail_font, secondary_color,
        (int(1218 * scale_x), int(159 * scale_y)),
        align="center"
    )
    
    # Render time
    render_text(
        screen, time_str, time_font, secondary_color,
        (int(363 * scale_x), int(174 * scale_y)), 
        align="center"
    )
    
    # Render dates
    render_text(
        screen, dates, detail_font, primary_color,
        (int(363 * scale_x), int(68 * scale_y)),
        align="center"
    )