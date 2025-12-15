# fetch_data.py

import os
import csv
import requests
from datetime import datetime, timedelta
from config import CSV_PATH, API, DATA

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
        print(f"\nError fetching data from API: {e}\n")
        return None

def fetch_prayer_data():
    """Fetch prayer data for the current and next month."""
    
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
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

def cache_status():
    """Check if the cached data has exceeded the cache duration."""
    
    cache_duration = DATA['CACHE_DURATION']
    
    # If CSV file does not exist, fetch new data
    if not os.path.exists(CSV_PATH):
        return True
    
    # Get the CSV file's last modification time
    file_mod_time = os.path.getmtime(CSV_PATH)
    file_mod_datetime = datetime.fromtimestamp(file_mod_time)
    
    # Calculate age of cached data in days
    cached_data_age = (datetime.now() - file_mod_datetime).days
    
    # Fetch new data if age of cached data exceeds cache duration
    return cached_data_age >= cache_duration

def save_data(data):
    """Saves fetched Adhan prayer data to CSV file, including calculated Iqamah times."""
    
    today = datetime.now().date()
    prayer_data = []
    
    # API prayer keys
    keys = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
    
    prayers = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha", "Jummah"]
    
    jummah_adhan = DATA['JUMMAH']['ADHAN']
    
    iqamah_offsets = DATA['IQAMAH_OFFSETS']
    
    fetch_buffer = DATA['FETCH_BUFFER']
    
    for day in data:
        
        # AlAdhan uses 'readable' date format (e.g., 01 Dec 2025)
        date_str = day['date']['readable']
        
        # Parse the date object from the API response string
        try:
            day_date_obj = datetime.strptime(date_str, "%d %b %Y").date()
        except ValueError:
            print(f"\nError parsing date: {date_str}\n")
            continue
        
        # Filter and buffer logic:
        
        # 1. Skip past dates, only start processing from today
        if day_date_obj < today:
            continue
        # 2. Check if we have reached the end of our buffer (e.g., 35 days)
        if len(prayer_data) >= fetch_buffer:
            break
        
        adhan_times = {}
        iqamah_times = {}
        
        # Parse and format prayer times from API response
        for prayer_name in keys:
            timing_str = day['timings'].get(prayer_name, "")
            if not timing_str:
                adhan_times[prayer_name] = ""
                iqamah_times[prayer_name] = ""
                continue
            
            # Strip timezone info
            time_24h = timing_str.split(" ")[0]
            
            # Process Sunrise and regular prayers
            if prayer_name == "Sunrise":
                try:
                    sunrise_time = datetime.strptime(time_24h, "%H:%M").strftime("%I:%M %p")
                except ValueError:
                    print(f"\nError parsing Sunrise time: {time_24h}\n")
                    sunrise_time = ""
                adhan_times[prayer_name] = sunrise_time
                iqamah_times[prayer_name] = ""
            else:
                # Parse date with 24-hour time
                try:
                    adhan_datetime = datetime.strptime(f"{date_str} {time_24h}", "%d %b %Y %H:%M")
                    adhan_times[prayer_name] = adhan_datetime.strftime("%I:%M %p")
                except ValueError:
                    print(f"\nError parsing {prayer_name} time: {time_24h}\n")
                    adhan_times[prayer_name] = ""
                    iqamah_times[prayer_name] = ""
                    continue
                
                # Calculate Iqamah times by adding offset
                offset_minutes = int(iqamah_offsets[prayer_name.upper()])
                iqamah_datetime = adhan_datetime + timedelta(minutes=offset_minutes)
                iqamah_times[prayer_name] = iqamah_datetime.strftime("%I:%M %p")
        
        # Process Jummah prayer
        try:
            jummah_datetime = datetime.strptime(f"{date_str} {jummah_adhan}", "%d %b %Y %I:%M %p")
            jummah_adhan_time = jummah_datetime.strftime("%I:%M %p")
        except ValueError:
            print(f"\nError parsing Jummah adhan time: {jummah_adhan}\n")
            jummah_adhan_time = ""
            jummah_datetime = None
        
        # Calculate Jummah Iqamah time
        jummah_offset_minutes = int(iqamah_offsets["JUMMAH"])
        if jummah_datetime:
            jummah_iqamah_datetime = jummah_datetime + timedelta(minutes=jummah_offset_minutes)
            jummah_iqamah_time = jummah_iqamah_datetime.strftime("%I:%M %p")
        else:
            jummah_iqamah_time = ""
        
        # Build CSV row: Date, then Adhan/Iqamah for each prayer (Sunrise only Adhan)
        row = [date_str]
        for prayer_name in prayers:
            if prayer_name == "Sunrise":
                row.append(adhan_times.get(prayer_name, ""))
            elif prayer_name == "Jummah":
                row.append(jummah_adhan_time)
                row.append(jummah_iqamah_time)
            else:
                row.append(adhan_times.get(prayer_name, ""))
                row.append(iqamah_times.get(prayer_name, ""))
        prayer_data.append(row)
    
    # Build CSV header: Date, then Adhan/Iqamah columns (Sunrise only Adhan)
    header_row = ["Date"]
    for prayer_name in prayers:
        if prayer_name == "Sunrise":
            header_row.append("Sunrise")
        else:
            header_row.append(f"{prayer_name}_Adhan")
            header_row.append(f"{prayer_name}_Iqamah")
    
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
    """Main function to check cache status and fetch data if needed."""    
    
    if cache_status():
        print(f"\nCache data is outdated/missing. Fetching data...\n")
        data = fetch_prayer_data()
        if data:
            save_data(data)
        else:
            print("\nError: No data fetched from API.\n")
    else:
        print(f"\nCache data is valid. Skipping fetch.\n")

if __name__ == "__main__":
    main()