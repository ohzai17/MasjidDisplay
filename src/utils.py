# utils.py

import csv
from datetime import datetime, timedelta
from config import CSV_PATH, DATA

def get_prayer_times():
    """Load prayer times from CSV file."""
    
    date = datetime.now()
    date_str = date.strftime("%d %b %Y")  # Format: "16 Dec 2025"
    
    try:
        with open(CSV_PATH, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Date'].strip() == date_str:
                    return dict(row)
    except FileNotFoundError:
        print(f"\nCSV file not found: {CSV_PATH}\n")
    
    return None

def apply_manual_override(prayer_name: str, api_time: str):
    """Return manual override if available, otherwise return API time."""
    
    if not api_time or not api_time.strip():
        return ""
    
    adhan_times = DATA['ADHAN_TIMES']
    manual_time = adhan_times.get(prayer_name.upper(), "").strip()
    
    return manual_time if manual_time else api_time

def format_prayer_table(prayer_times):
    """Format prayer times into a table."""
    
    def format_time(value):
        """Validate and format time string."""
        if not value or not value.strip():
            return "––––––––––"
        
        return value.strip()
    
    if not prayer_times:
        prayer_times = {}
    
    prayers = [
        ("Fajr", "Fajr"),
        ("Sunrise", "Sunrise"),
        ("Dhuhr", "Dhuhr"),
        ("Asr", "Asr"),
        ("Maghrib", "Maghrib"),
        ("Isha", "Isha"),
    ]
    
    prayer_data = prayer_times
    formatted_prayer_times = []
    
    PLACEHOLDER = "––––––––––"
    
    date_str = prayer_times.get('Date', '')
    iqamah_offsets = DATA['IQAMAH_OFFSETS']
    
    for prayer_name, csv_key in prayers:
        
        api_time = prayer_data.get(csv_key, '')
        adhan_time = format_time(apply_manual_override(prayer_name, api_time))
        iqamah_time = PLACEHOLDER
        
        # Calculate Iqamah time
        if adhan_time != PLACEHOLDER:
            try:
                adhan_datetime = datetime.strptime(f"{date_str} {adhan_time}", "%d %b %Y %I:%M %p")
                offset_minutes = int(iqamah_offsets[prayer_name.upper()])
                iqamah_datetime = adhan_datetime + timedelta(minutes=offset_minutes)
                iqamah_time = iqamah_datetime.strftime("%I:%M %p")
            except (ValueError, KeyError):
                pass
        else:
            iqamah_time = PLACEHOLDER
        
        formatted_prayer_times.append((prayer_name, adhan_time, iqamah_time))
    
    # Handle Jummah
    jummah = DATA['JUMMAH']
    jummah_adhan = jummah.get('ADHAN_TIME', '').strip()
    jummah_iqamah_offset = jummah.get('IQAMAH_OFFSET')
    
    if jummah_adhan:
        try:
            jummah_datetime = datetime.strptime(f"{date_str} {jummah_adhan}", "%d %b %Y %I:%M %p")
            jummah_adhan_time = jummah_datetime.strftime("%I:%M %p")
            jummah_iqamah_datetime = jummah_datetime + timedelta(minutes=jummah_iqamah_offset)
            jummah_iqamah_time = jummah_iqamah_datetime.strftime("%I:%M %p")
            
            formatted_prayer_times.append(("Jummah", jummah_adhan_time, jummah_iqamah_time))
        except (ValueError, KeyError):
            formatted_prayer_times.append(("Jummah", PLACEHOLDER, PLACEHOLDER))
    else:
        formatted_prayer_times.append(("Jummah", PLACEHOLDER, PLACEHOLDER))
    
    return formatted_prayer_times

def get_next_prayer(now):
    """Find the next prayer after current time."""
    
    def parse_time(time_str):
        """Convert time string to datetime object."""
        try:
            return datetime.strptime(time_str.strip(), "%I:%M %p").time()
        except ValueError:
            return None
    
    prayer_times = get_prayer_times()
    
    if not prayer_times:
        return None, None
    
    prayers = [
        ("Fajr", "Fajr"),
        ("Dhuhr", "Dhuhr"),
        ("Asr", "Asr"),
        ("Maghrib", "Maghrib"),
        ("Isha", "Isha"),
    ]
    
    for prayer_name, adhan_key in prayers:
        adhan_time_str = prayer_times.get(adhan_key, "")
        adhan_time = parse_time(adhan_time_str)
        
        if adhan_time:
            adhan_datetime = datetime.combine(now.date(), adhan_time)
            
            # Check if this prayer is still today (in the future)
            if adhan_datetime > now:
                return prayer_name, adhan_datetime
    
    # If all prayers for today have passed, return Fajr of next day
    adhan_time_str = prayer_times.get("Fajr", "")
    adhan_time = parse_time(adhan_time_str)
    if adhan_time:
        next_prayer_time = datetime.combine(now.date(), adhan_time) + timedelta(days=1)
        return "Fajr", next_prayer_time
    
    return None, None