# table.py

import csv
import pygame
from datetime import datetime

def get_prayer_times():
    """Load prayer times for today from the CSV file."""
    
    date = datetime.now()
    date_str = date.strftime("%d %b %Y")  # Format: "16 Dec 2025"
    
    try:
        with open(CSV_PATH, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Date'].strip() == date_str:
                    return dict(row)
    except FileNotFoundError:
        print(f"\nPrayer times file not found: {CSV_PATH}\n")
    
    return None

def format_prayer_times(prayer_times_data):
    """Format prayer times into a table."""
    
    def format_time(value):
        """Validate and format time string."""
        if not value or not value.strip():
            return "––––––––––"
        
        return value.strip()
    
    if not prayer_times_data:
        prayer_times_data = {}
    
    prayers = [
        ("Fajr", "Fajr_Adhan", "Fajr_Iqamah"),
        ("Sunrise", "Sunrise", None),
        ("Dhuhr", "Dhuhr_Adhan", "Dhuhr_Iqamah"),
        ("Asr", "Asr_Adhan", "Asr_Iqamah"),
        ("Maghrib", "Maghrib_Adhan", "Maghrib_Iqamah"),
        ("Isha", "Isha_Adhan", "Isha_Iqamah"),
        ("Jummah", "Jummah_Adhan", "Jummah_Iqamah"),
    ]
    
    prayer_times = [
        (name, 
        format_time(prayer_times_data.get(adhan, '')), 
        format_time(prayer_times_data.get(iqamah, '')) if iqamah else "––––––––––")
        for name, adhan, iqamah in prayers
    ]
    
    return prayer_times