# display.py

from hijridate import Gregorian
from config import HIJRI_MONTH_NAMES, NAME, ADDRESS, BLACK_COLOR, FOREST_GREEN_COLOR
from utils import render_text

def render_main(screen, current_datetime, scale_x, scale_y, time_font, title_font, detail_font):
    """Render main display."""
    
    # Time and date formatting
    time_str = current_datetime.strftime("%I:%M:%S %p")
    date_str = current_datetime.strftime("%d %B %Y")
    
    # Get the Hijri date
    hijri_date = Gregorian(current_datetime.year, current_datetime.month, current_datetime.day).to_hijri()
    hijri_month_name = HIJRI_MONTH_NAMES[hijri_date.month]
    hijri_str = f"{hijri_date.day:02d} {hijri_month_name} {hijri_date.year}"
    
    dates = date_str + " · " + hijri_str # Combine Gregorian and Hijri dates
    
    # Render name
    render_text(
        screen, NAME, title_font, FOREST_GREEN_COLOR,
        (int(1218 * scale_x), int(86 * scale_y)), 
        align="center"
    )
    
    # Render address
    render_text(
        screen, ADDRESS, detail_font, BLACK_COLOR,
        (int(1218 * scale_x), int(159 * scale_y)),
        align="center"
    )
    
    # Render time
    render_text(
        screen, time_str, time_font, BLACK_COLOR,
        (int(363 * scale_x), int(174 * scale_y)), 
        align="center"
    )
    
    # Render dates
    render_text(
        screen, dates, detail_font, FOREST_GREEN_COLOR,
        (int(363 * scale_x), int(68 * scale_y)),
        align="center"
    )