# data.py

import os
import csv
import requests
from datetime import datetime, timedelta
from config import CSV_PATH, API, DATA

def fetch_data():
    """Fetch prayer data from the API."""
    
    prayer_times = []
    current_date = datetime.now()
    end_date = current_date + timedelta(days=DATA['FETCH_WINDOW'])
    
    month, year = current_date.month, current_date.year
    
    while datetime(year, month, 1) <= end_date:
        
        params = {
            'city': API['LOCATION']['CITY'],
            'country': API['LOCATION']['COUNTRY'],
            'timezone': API['LOCATION'].get('TIMEZONE', ''),
            'latitude': API['LOCATION']['LATITUDE'],
            'longitude': API['LOCATION']['LONGITUDE'],
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
            response = requests.get(API['ENDPOINT'], params=params)
            response.raise_for_status()
            prayer_times.extend(response.json()['data'])
        except requests.RequestException as e:
            print(f"\nError fetching data from API: {e}")
        
        month += 1
        if month > 12:
            month = 1
            year += 1
    
    return prayer_times

def format_time(api_time_str: str) -> str:
    """Convert 24-hour format to 12-hour AM/PM format."""
    
    if not api_time_str:
        return ""
    
    # API returns time with timezone info, e.g., "05:30 (GMT)"
    try:
        api_time = api_time_str.split(" ")[0]
        return datetime.strptime(api_time, "%H:%M").strftime("%I:%M %p")
    except ValueError:
        return ""

def cache_status():
    """Check if cached data needs to be refreshed."""
    
    # If CSV file does not exist, fetch new data
    if not os.path.exists(CSV_PATH):
        return True, 0
    
    file_age = (datetime.now() - datetime.fromtimestamp(os.path.getmtime(CSV_PATH))).days
    
    # Fetch new data if age of cached data exceeds refresh interval (e.g., 30 days)
    return file_age >= DATA['REFRESH_INTERVAL'], file_age

def save_to_csv(prayer_times):
    """Save prayer data to CSV file."""
    
    today = datetime.now().date()
    rows = []
    
    prayer_keys = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
    
    fetch_window = DATA['FETCH_WINDOW']
    
    for day in prayer_times:
        
        # AlAdhan uses 'readable' date format (e.g., 01 Dec 2025)
        date_str = day['date']['readable']
        
        # Parse date to filter by today and fetch window
        try:
            date_obj = datetime.strptime(date_str, "%d %b %Y").date()
        except ValueError:
            continue
        
        # Skip dates before today and limit to fetch window (e.g., 35 days)
        if date_obj < today:
            continue
        if len(rows) >= fetch_window:
            break
        
        row = [date_str]
        for prayer in prayer_keys:
            row.append(format_time(day['timings'].get(prayer, "")))
        rows.append(row)
    
    # CSV Header: Date, Fajr, Sunrise, Dhuhr, Asr, Maghrib, Isha
    try:
        with open(CSV_PATH, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"])
            writer.writerows(rows)
        print(f"\nPrayer data saved to {CSV_PATH}.\n")
        return True
    except IOError as e:
        print(f"\nError saving data to CSV: {e}\n")
        return False

def main():
    """Fetch and save prayer times if needed."""
    
    needs_fetch, file_age = cache_status()
    
    if not needs_fetch:
        days_left = DATA['REFRESH_INTERVAL'] - file_age
        print(f"\nCache data is up-to-date. There are {days_left} days left. Skipping fetch.\n")
        return
    
    print(f"\nFetching prayer times...")
    prayer_times = fetch_data()
    
    if prayer_times:
        save_to_csv(prayer_times)
    else:
        print("\nError: No data fetched from API.")

if __name__ == "__main__":
    main()