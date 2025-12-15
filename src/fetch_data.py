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
        print(f"\nError fetching data from API: {e}")
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
    
    # Fetch new data if age of cached data exceeds cache duration (e.g., 30 days)
    return cached_data_age >= cache_duration

def get_prayer_time(prayer_name: str, api_time_str: str, date_str: str):
    """Format and return prayer time, considering manual overrides."""
    
    adhan_times_manual = DATA['ADHAN_TIMES_MANUAL']
    
    # Check if manual time is present in settings
    adhan_time_manual = adhan_times_manual.get(prayer_name.upper(), "").strip()
    
    if adhan_time_manual:
        try:
            adhan_datetime = datetime.strptime(f"{date_str} {adhan_time_manual}", "%d %b %Y %I:%M %p")
            adhan_time_formatted = adhan_datetime.strftime("%I:%M %p")
            return adhan_time_formatted, adhan_datetime
        except ValueError:
            print(f"\nError parsing {prayer_name} time: {adhan_time_manual}")
            pass
    
    # Use API time (either no manual time or manual time failed to parse)
    if not api_time_str:
        return "", None
    
    api_time = api_time_str.split(" ")[0] # Strip timezone info
    
    try:
        adhan_datetime = datetime.strptime(f"{date_str} {api_time}", "%d %b %Y %H:%M")
        adhan_time_formatted = adhan_datetime.strftime("%I:%M %p")
        return adhan_time_formatted, adhan_datetime
    except ValueError:
        print(f"\nError parsing {prayer_name} time from API: {api_time}")
        return "", None

def save_data(data):
    """Saves fetched Adhan prayer data to CSV file, including calculated Iqamah times."""
    
    today = datetime.now().date()
    prayer_data = []
    
    # API prayer keys
    keys = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
    
    prayers = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha", "Jummah"]
    
    adhan_times_manual = DATA['ADHAN_TIMES_MANUAL']
    iqamah_offsets = DATA['IQAMAH_OFFSETS']
    
    fetch_buffer = DATA['FETCH_BUFFER']
    
    for day in data:
        
        # AlAdhan uses 'readable' date format (e.g., 01 Dec 2025)
        date_str = day['date']['readable']
        
        # Parse the date object from the API response string
        try:
            day_date_obj = datetime.strptime(date_str, "%d %b %Y").date()
        except ValueError:
            print(f"\nError parsing date: {date_str}")
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
            
            # Handle Sunrise
            if prayer_name == "Sunrise":
                if not timing_str:
                    adhan_times[prayer_name] = ""
                    iqamah_times[prayer_name] = ""
                    continue
                
                api_time = timing_str.split(" ")[0] # Strip timezone info
                
                try:
                    sunrise_time = datetime.strptime(api_time, "%H:%M").strftime("%I:%M %p")
                except ValueError:
                    print(f"\nError parsing Sunrise time from API: {api_time}")
                    sunrise_time = ""
                adhan_times[prayer_name] = sunrise_time
                iqamah_times[prayer_name] = "" # Set Iqamah to empty string
            
            # Handle regular prayers
            else:
                adhan_time_formatted, adhan_datetime = get_prayer_time(prayer_name, timing_str, date_str)
                
                # Store formatted adhan times in dict
                adhan_times[prayer_name] = adhan_time_formatted
                
                # Calculate Iqamah time by adding offset
                if adhan_datetime:
                    offset_minutes = int(iqamah_offsets[prayer_name.upper()])
                    iqamah_datetime = adhan_datetime + timedelta(minutes=offset_minutes)
                    iqamah_times[prayer_name] = iqamah_datetime.strftime("%I:%M %p")
                else:
                    iqamah_times[prayer_name] = ""
        
        # Handle Jummah
        manual_jummah_adhan_time = adhan_times_manual.get("JUMMAH", "").strip()
        
        if manual_jummah_adhan_time:
            try:
                jummah_datetime = datetime.strptime(f"{date_str} {manual_jummah_adhan_time}", "%d %b %Y %I:%M %p")
                jummah_adhan_time = jummah_datetime.strftime("%I:%M %p")
            except ValueError:
                print(f"\nError parsing Jummah time: {manual_jummah_adhan_time}")
                jummah_adhan_time = ""
                jummah_datetime = None
        else:
            jummah_adhan_time = ""
            jummah_datetime = None
        
        # Calculate Iqamah time by adding offset
        jummah_offset_minutes = int(iqamah_offsets["JUMMAH"])
        if jummah_datetime:
            jummah_iqamah_datetime = jummah_datetime + timedelta(minutes=jummah_offset_minutes)
            jummah_iqamah_time = jummah_iqamah_datetime.strftime("%I:%M %p")
        else:
            jummah_iqamah_time = ""
        
        # CSV row: Date, then Adhan and Iqamah for each prayer
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
    
    # CSV header: Date, then Adhan and Iqamah columns
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
        print(f"\nCache data is outdated or missing. Fetching data...\n")
        data = fetch_prayer_data()
        if data:
            save_data(data)
        else:
            print("\nError: No data fetched from API.")
    else:
        print(f"\nCache data is valid. Skipping fetch.\n")

if __name__ == "__main__":
    main()