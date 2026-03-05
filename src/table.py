# table.py

import csv
from arabic_reshaper import reshape
from datetime import datetime, timedelta
from config import CSV, load_settings
from bidi.algorithm import get_display
from utils import render_text, get_text_colors

def load_prayer_times():
    """Load today's prayer times from CSV."""
    
    today_str = datetime.now().strftime('%d %b %Y')
    
    try:
        with open(CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Date'].strip() == today_str:
                    return {k: v for k, v in row.items() if k != 'Date'}
    except FileNotFoundError:
        pass
    return {}

def format_table(prayer_times):
    """Format prayer times into a table."""
    
    settings = load_settings()
    
    DATA = settings['DATA']
    
    prayers = [
        "Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha", "Jummah"
    ]
    
    PLACEHOLDER = "––––––––––"
    formatted_prayer_times = []
    
    # If no CSV data for today, show placeholders for all prayers
    if not prayer_times:
        for prayer_name in prayers:
            formatted_prayer_times.append((prayer_name, PLACEHOLDER, PLACEHOLDER))
        return formatted_prayer_times
    
    for prayer_name in prayers:
        # Get the base time from CSV
        base_time = prayer_times.get(prayer_name, "")
        
        # Manual override from config
        manual_time = DATA["PRAYERS"].get(prayer_name.upper(), {}).get("ADHAN_TIME", "").strip()
        
        # No CSV column for Jummah
        if prayer_name == "Jummah":
            adhan_time = manual_time
        else:
            adhan_time = manual_time if manual_time else base_time
        
        # Format adhan time
        adhan_time = adhan_time.strip() if adhan_time and adhan_time.strip() else PLACEHOLDER
        
        # Calculate Iqamah time
        iqamah_time = PLACEHOLDER
        if adhan_time != PLACEHOLDER:
            iqamah_offset = DATA["PRAYERS"].get(prayer_name.upper(), {}).get("IQAMAH_OFFSET")
            try:
                adhan_dt = datetime.strptime(adhan_time, "%I:%M %p")
                iqamah_dt = adhan_dt + timedelta(minutes=iqamah_offset)
                iqamah_time = iqamah_dt.strftime("%I:%M %p")
            except Exception:
                pass
        
        formatted_prayer_times.append((prayer_name, adhan_time, iqamah_time))
    
    return formatted_prayer_times


def render_table(screen, scale_x, scale_y, table_font, arabic_font):
    """Render the prayer times table."""
    
    from countdown import get_next_event
    
    arabic_prayers = [
        "فجر", "شروق", "ظهر", "عصر", "مغرب", "عشاء", "جمعة"
    ]
    
    primary, secondary, tertiary = get_text_colors()
    
    now = datetime.now()
    
    prayer_times = load_prayer_times()
    formatted_prayer_times = format_table(prayer_times)
    
    # Determine the next event/prayer
    _, next_prayer, _ = get_next_event(now, formatted_prayer_times)
    
    # Table positioning
    table_start_x, table_start_y = int(58 * scale_x), int(298 * scale_y)
    vertical_spacing = int(table_font.get_height() * 1.0)
    
    # Column definitions: (width, align, header)
    columns = [
        (int(225 * scale_x), "left", "Prayer"),
        (int(185 * scale_x), "right", ""),
        (int(72 * scale_x), "center", "Adhan"),
        (int(385 * scale_x), "center", "Iqamah"),
    ]
    
    # Calculate x positions for each column
    col_x = [table_start_x]
    for width, _, _ in columns[:-1]:
        col_x.append(col_x[-1] + width)
    
    # Render header
    for idx, (width, align, header_text) in enumerate(columns):
        x = col_x[idx]
        if align == "center":
            x += width // 2
        
        if header_text == "Prayer":
            render_text(
                screen, header_text, table_font, primary,
                (x + 76, table_start_y), align=align, shadow_color=tertiary
            )
        else:
            render_text(
                screen, header_text, table_font, primary,
                (x, table_start_y), align=align, shadow_color=tertiary
            )
    
    # Render prayer rows
    for i, (prayer_name, adhan, iqamah) in enumerate(formatted_prayer_times):
        y = table_start_y + ((i + 1) * vertical_spacing)
        
        if prayer_name == next_prayer:
            font_color = primary
        else:
            font_color = secondary
        
        # Render prayer name
        render_text(
            screen, prayer_name, table_font, primary,
            (col_x[0], y), align=columns[0][1],
            shadow_color=tertiary
        )
        
        # Reshape and apply bidi algorithm for proper Arabic rendering
        arabic_prayer_name = get_display(reshape(arabic_prayers[i]))
        
        # Render prayer name (Arabic)
        x = col_x[1] + columns[1][0] // 2
        render_text(
            screen, arabic_prayer_name, arabic_font, primary,
            (x, y - 4), align=columns[1][1],
            shadow_color=tertiary # Slight vertical adjustment
        )
        
        # Render Adhan
        x = col_x[2] + columns[2][0] // 2
        render_text(
            screen, adhan, table_font, font_color,
            (x, y), align=columns[2][1],
            shadow_color=tertiary
        )
        
        # Render Iqamah
        x = col_x[3] + columns[3][0] // 2
        render_text(
            screen, iqamah, table_font, font_color,
            (x, y), align=columns[3][1], 
            shadow_color=tertiary
        )