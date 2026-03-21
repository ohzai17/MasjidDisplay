# table.py

from datetime import datetime
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from src.utils import (
    load_prayer_times, get_prayer_times, get_next_event, get_text_colors, render_text)

def render_table(screen, scale_x, scale_y, table_font, arabic_font):
    """Render the prayer times table."""
    
    arabic_prayers = [
        "فجر", "شروق", "ظهر", "عصر", "مغرب", "عشاء", "جمعة"
    ]
    
    primary, secondary, tertiary = get_text_colors()
    
    now = datetime.now()
    
    prayer_times = load_prayer_times()
    formatted_prayer_times = get_prayer_times(prayer_times)
    
    # Determine the next event/prayer
    _, next_prayer, _ = get_next_event(now, formatted_prayer_times)
    
    # Table positioning
    table_start_x, table_start_y = int(58 * scale_x), int(298 * scale_y)
    vertical_spacing = int(table_font.get_height() * 1.0)
    
    # Column definitions: (width, align, header)
    columns = [
        (int(225 * scale_x), "left", "Prayer"),
        (int(185 * scale_x), "right", ""),
        (int(85 * scale_x), "center", "Adhan"),
        (int(345 * scale_x), "center", "Iqamah"),
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
                (x + int(90 * scale_x), table_start_y), align=align,
                shadow_color=tertiary
            )
        else:
            render_text(
                screen, header_text, table_font, primary,
                (x, table_start_y), align=align,
                shadow_color=tertiary
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
            screen, arabic_prayer_name, arabic_font, secondary,
            (x + int(4 * scale_x), y - int(12 * scale_y)), align=columns[1][1],
            shadow_color=tertiary
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