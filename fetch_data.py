# fetch_data.py

import csv
import json
import requests
from datetime import datetime

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
    data = data_current + data_next
    
    return data

def save_data(data):
    """Saves fetched Adhan prayer data to CSV file, including Jummah time."""
    
    today = datetime.now().date()
    prayer_data = []
    
    keys = ["Fajr", "Sunrise","Dhuhr", "Asr", "Maghrib", "Isha"]
    
    jummah_adhan = settings['DATA']['JUMMAH']['ADHAN']
    jummah_iqamah = settings['DATA']['JUMMAH']['IQAMAH']
    
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
        if len(prayer_data) >= DATA['FETCH_DAYS_BUFFER']:
            break
        
        # Start the row with the date
        row = [date_str_readable]
        
        adhan_times = []
        for prayer_name in keys:
            # Convert 24-hour time to 12-hour format with AM/PM
            adhan_str = datetime.strptime(day['timings'][prayer_name].split(" ")[0], "%H:%M").strftime("%I:%M %p")
            adhan_times.append(adhan_str)

        jummah_adhan_str = datetime.strptime(jummah_adhan, "%I:%M %p")
        jummah_iqamah_str = datetime.strptime(jummah_iqamah, "%I:%M %p")

        row.extend(adhan_times)
        
        row.append(jummah_adhan)
        
        prayer_data.append(row)
        
    prayers = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha", "Jummah"]
    
    header_row = ["Date"] + [p if p == "Sunrise" else f"{p}_Adhan" for p in prayers]
    
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