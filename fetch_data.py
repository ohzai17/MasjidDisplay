# fetch_data.py

import csv
import json
import requests
from datetime import datetime, timedelta

SETTINGS_PATH = 'assets/settings.json'
CSV_PATH = 'assets/prayer_times.csv'

def load_settings():
    """Load settings from JSON file."""
    with open(SETTINGS_PATH, 'r') as file:
        return json.load(file)

settings = load_settings()
API = settings['API']
DATA = settings['DATA']

def fetch_month_data(month: int, year: int):
    """Fetch prayer times from the AlAdhan API for a given month and year."""
    
    url = API['ENDPOINT']
    
    params = {
        'city': API['LOCATION']['CITY'],
        'country': API['LOCATION']['COUNTRY'],
        'latitude': API['LOCATION']['LATITUDE'],
        'longitude': API['LOCATION']['LONGITUDE'],
        'adjustment': API['HIJRI_DATE']['ADJUSTMENT'],
        'method': API['CALCULATION']['METHOD'],
        'school': API['CALCULATION']['SCHOOL'],
        'month': month,
        'year': year,
    }
    
    # Custom angles for Fajr and Isha if method is 99 (Custom)
    if API['CALCULATION']['METHOD'] == 99:
        params['fajr'] = API['ANGLES']['FAJR']
        params['isha'] = API['ANGLES']['ISHA']
        
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data['data']
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def fetch_prayer_data():
    """Fetch prayer data for the current and next month."""
    
    today = datetime.now()
    current_month = today.month
    current_year = today.year
    
    # Calculate next month and year
    if current_month == 12:
        next_month = 1
        next_year = current_year + 1
    else:
        next_month = current_month + 1
        next_year = current_year
        
    # Fetch data for both months
    data_current = fetch_month_data(current_month, current_year)
    data_next = fetch_month_data(next_month, next_year)
    
    # Join data
    data = (data_current or []) + (data_next or [])
    
    return data

def save_data(data):
    """Saves fetched Adhan prayer data to CSV file, including calculated Iqamah times."""
    
    today = datetime.now().date()
    prayer_data = []
    
    # API prayer keys
    keys = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
    
    # Jummah times (adhan is configured in settings)
    jummah_adhan_setting = settings['DATA']['JUMMAH']['ADHAN']

    iqamah_offsets = DATA.get('IQAMAH_OFFSETS', {})
    fetch_buffer = DATA.get('FETCH_DAYS_BUFFER', 35)

    prayers = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha", "Jummah"]

    for day in data:
        
        # AlAdhan uses 'readable' date format (e.g., 02 Dec 2025)
        date_str_readable = day['date']['readable']
        
        # Parse the date object from the API response string
        try:
            day_date_obj = datetime.strptime(date_str_readable, "%d %b %Y").date()
        except ValueError:
            print(f"Error parsing date: {date_str_readable}")
            continue
        
        # 1. Skip past dates, only start processing from today
        if day_date_obj < today:
            continue
        
        # 2. Check if we have reached the end of our buffer (e.g., 35 days)
        if len(prayer_data) >= fetch_buffer:
            break
        
        # Dicts to store adhan and iqamah strings per prayer
        adhan_times = {}
        iqamah_times = {}
        
        # Process regular prayers from API
        for prayer_name in keys:
            raw_timing = day['timings'].get(prayer_name, "")
            if not raw_timing:
                adhan_times[prayer_name] = ""
                iqamah_times[prayer_name] = ""
                continue
            
            # API timing may include timezone info (e.g., "05:00 (EDT)"), so take first token
            time_token = raw_timing.split(" ")[0]
            
            # Sunrise only has adhan (no iqamah)
            if prayer_name == "Sunrise":
                try:
                    adhan_formatted = datetime.strptime(time_token, "%H:%M").strftime("%I:%M %p")
                except ValueError:
                    adhan_formatted = ""
                adhan_times[prayer_name] = adhan_formatted
                iqamah_times[prayer_name] = ""
            else:
                # Combine date with 24-hour time to ensure correct day/time
                try:
                    adhan_dt = datetime.strptime(f"{date_str_readable} {time_token}", "%d %b %Y %H:%M")
                    adhan_times[prayer_name] = adhan_dt.strftime("%I:%M %p")
                except ValueError:
                    adhan_times[prayer_name] = ""
                    iqamah_times[prayer_name] = ""
                    continue
                
                # Compute iqamah using offset minutes from settings (default 0)
                offset_minutes = int(iqamah_offsets.get(prayer_name.upper(), 0))
                iqamah_dt = adhan_dt + timedelta(minutes=offset_minutes)
                iqamah_times[prayer_name] = iqamah_dt.strftime("%I:%M %p")
        
        # Process Jummah (use configured adhan time and compute iqamah by offset)
        try:
            jummah_dt = datetime.strptime(f"{date_str_readable} {jummah_adhan_setting}", "%d %b %Y %I:%M %p")
            jummah_adhan_formatted = jummah_dt.strftime("%I:%M %p")
        except ValueError:
            # Fallback: empty if parsing fails
            jummah_adhan_formatted = jummah_adhan_setting or ""
            jummah_dt = None
        
        jummah_offset = int(iqamah_offsets.get("JUMMAH", 0))
        if jummah_dt:
            jummah_iqamah_formatted = (jummah_dt + timedelta(minutes=jummah_offset)).strftime("%I:%M %p")
        else:
            # If jummah_dt couldn't be parsed, fall back to configured IQAMAH if present
            jummah_iqamah_formatted = settings['DATA']['JUMMAH'].get('IQAMAH', "")
        
        # Build CSV row with columns grouped per-prayer (Adhan then Iqamah)
        row = [date_str_readable]
        for p in prayers:
            if p == "Sunrise":
                row.append(adhan_times.get(p, ""))
            elif p == "Jummah":
                row.append(jummah_adhan_formatted)
                row.append(jummah_iqamah_formatted)
            else:
                row.append(adhan_times.get(p, ""))
                row.append(iqamah_times.get(p, ""))
        
        prayer_data.append(row)
        
    # Build header: Date, then for each prayer include Adhan and Iqamah adjacent (Sunrise only adhan)
    header_row = ["Date"]
    for p in prayers:
        if p == "Sunrise":
            header_row.append("Sunrise")
        else:
            header_row.append(f"{p}_Adhan")
            header_row.append(f"{p}_Iqamah")

    try:
        with open(CSV_PATH, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header_row)
            writer.writerows(prayer_data)
        print(f"\nPrayer data saved to {CSV_PATH}.\n")
        return True
    except IOError as e:
        print(f"\nError saving data to CSV: {e}\n")
        return False


def main():
    data = fetch_prayer_data()
    if data:
        save_data(data)
    else:
        print("No data fetched.")

if __name__ == "__main__":
    main()