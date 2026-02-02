# data.py

import os
import csv
from praytimes import PrayTimes
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, time, date
from .config import (
    CSV, LATITUDE, LONGITUDE, TIMEZONE, 
    CALCULATION_METHOD, ASR_METHOD
)

def format_time(t):
    """Convert time from 24-hour to 12-hour format with AM/PM."""
    
    try:
        return datetime.strptime(t, "%H:%M").strftime("%I:%M %p")
    except Exception:
        return t

def fetch_data(start_date=date.today(), days=365):
    """Fetch data from PrayTimes library."""
    
    pt = PrayTimes(CALCULATION_METHOD)
    pt.adjust({'asr': ASR_METHOD})
    pt.adjust({'maghrib': '0 min'})
    
    rows = []
    header = ["Date", "Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
    rows.append(header)
    
    for i in range(days):
        date_iter = start_date + timedelta(days=i)
        dt_with_time = datetime.combine(date_iter, time(12, 0))
        try:
            offset = dt_with_time.astimezone(ZoneInfo(TIMEZONE)).utcoffset()
            tz_offset = int(offset.total_seconds() // 3600) if offset is not None else 0
            times = pt.getTimes(
                [date_iter.year, date_iter.month, date_iter.day],
                [LATITUDE, LONGITUDE],
                tz_offset
            )
            row = [
                date_iter.strftime('%d %b %Y'),
                format_time(times['fajr']),
                format_time(times['sunrise']),
                format_time(times['dhuhr']),
                format_time(times['asr']),
                format_time(times['maghrib']),
                format_time(times['isha'])
            ]
            rows.append(row)
        except Exception as e:
            print(f"Error fetching data for {date_iter}: {e}.")
            continue
    return rows

def save_data(rows, csv_path=CSV):
    """Save fetched data to CSV file."""
    
    try:
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print(f"Data saved to {csv_path}")
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def main():
    """Fetch and save prayer times if needed."""
    
    rows = fetch_data()
    save_data(rows)

if __name__ == "__main__":
    main()