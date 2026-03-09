# data.py

# Based on the PrayTimes JavaScript library by Hamid Zarrabi-Zadeh
# Original source: https://praytimes.org/docs/calculation

import csv
import math
from src.config import CSV
from zoneinfo import ZoneInfo
from src.utils import load_settings
from datetime import datetime, timedelta

class PrayerTimes:
    """
    Calculates Islamic prayer times based on astronomical formulas.
    Supports multiple calculation methods and juristic preferences.
    """
    
    def __init__(self, method):
        
        # Calculation Methods
        self.methods = {
            'ISNA': {'fajr': 15, 'isha': 15},
            'MWL': {'fajr': 18, 'isha': 17},
            'Egypt': {'fajr': 19.5, 'isha': 17.5},
            'Makkah': {'fajr': 18.5, 'isha': '90 min'},
            'Karachi': {'fajr': 18, 'isha': 18},
            'Tehran': {'fajr': 17.7, 'isha': 14},
            'Jafari': {'fajr': 16, 'isha': 14},
            'France': {'fajr': 12, 'isha': 12},
            'Russia': {'fajr': 16, 'isha': 15},
            'Singapore': {'fajr': 20, 'isha': 18}
        }
        
        # Set calculation method and settings
        self.calcMethod = method
        self.settings = self.methods[method]
        
        # Juristic method for Asr: Standard (0) or Hanafi (1)
        self.asrJuristic = 0
        
        # Minute offsets for all prayers
        self.fajrMinutes = 0
        self.dhuhrMinutes = 0
        self.asrMinutes = 0
        self.maghribMinutes = 0
        self.ishaMinutes = 0
    
    def setMethod(self, method):
        """Change calculation method."""
        
        if method in self.methods:
            self.settings = self.methods[method]
            self.calcMethod = method
    
    def setAsrMethod(self, method):
        """Set Asr juristic method: 'Hanafi' or 'Standard (Shafi, Maliki, Hanbali)'."""
        
        if method == 'Hanafi':
            self.asrJuristic = 1
        else:
            self.asrJuristic = 0
    
    def getTimes(self, date, coords, timezone_offset):
        """Main entry: Calculate prayer times for a given date, coordinates, and timezone."""
        
        self.lat = coords[0]
        self.lng = coords[1]
        self.timezone_offset = timezone_offset
        self.jDate = self.julian(date.year, date.month, date.day) - self.lng / (15 * 24.0)
        return self.computeTimes()
    
    def computeTimes(self):
        """Estimate prayer times (in float hours) for the day."""
        
        # Initial guess for times (in 24-hour format)
        times = {
            'Fajr': 5,
            'Sunrise': 6,
            'Dhuhr': 12,
            'Asr': 13,
            'Sunset': 18,
            'Maghrib': 18,
            'Isha': 18
        }
        
        # Calculate times using astronomical formulas
        times = self.computePrayerTimes(times)
        
        # Adjust for timezone and custom offsets
        times = self.adjustTimes(times)
        
        return times
    
    def computePrayerTimes(self, times):
        """Calculate prayer times using sun angles and astronomical formulas."""
        
        # Convert times to day portions (fractional day)
        times = self.dayPortion(times)
        params = self.settings
        
        # Calculate each prayer time
        fajr = self.sunAngleTime(params['fajr'], times['Fajr'], 'ccw')
        sunrise = self.sunAngleTime(self.riseSetAngle(), times['Sunrise'], 'ccw')
        dhuhr = self.midDay(times['Dhuhr'])
        asr = self.asrTime(self.asrJuristic + 1, times['Asr'])
        sunset = self.sunAngleTime(self.riseSetAngle(), times['Sunset'])
        
        # Maghrib: Standard calculation is to use the time of sunset as Maghrib.
        maghrib = sunset
        
        # Alternative Maghrib calculation: Calculate Maghrib using a fixed sun angle (4° below horizon) instead of sunset. 
        # maghrib = self.sunAngleTime(4, times['Maghrib']) if self.maghribMinutes else sunset
        
        # Isha: If method uses minutes after sunset, add minutes; else, use sun angle
        if isinstance(params['isha'], str) and "min" in params['isha']:
            minutes = float(params['isha'].split()[0])
            isha = sunset + minutes / 60.0 # Add custom minutes after sunset
        else:
            isha = self.sunAngleTime(params['isha'], times['Isha'])
        
        return {
            'Fajr': fajr,
            'Sunrise': sunrise,
            'Dhuhr': dhuhr,
            'Asr': asr,
            'Sunset': sunset,
            'Maghrib': maghrib,
            'Isha': isha
        }
    
    def adjustTimes(self, times):
        """Adjust times for timezone, longitude, and custom minute offsets."""
        
        for key in times:
            
            # Adjust for timezone and longitude
            times[key] += self.timezone_offset - self.lng / 15.0
        
        # Apply custom minute adjustments
        if self.fajrMinutes:
            times['Fajr'] += self.fajrMinutes / 60.0
        if self.dhuhrMinutes:
            times['Dhuhr'] += self.dhuhrMinutes / 60.0
        if self.asrMinutes:
            times['Asr'] += self.asrMinutes / 60.0
        if self.maghribMinutes:
            times['Maghrib'] += self.maghribMinutes / 60.0
        if self.ishaMinutes:
            times['Isha'] += self.ishaMinutes / 60.0
        
        return times
    
    def sunAngleTime(self, angle, time, direction='cw'):
        """
        Calculate time when sun reaches a specific angle below the horizon.
        Used for Fajr, Sunrise, Sunset, Isha, etc.
        """
        
        decl = self.sunPosition(self.jDate + time)[0]
        noon = self.midDay(time)
        t = (1/15.0) * self.arccos((-self.sin(angle) - self.sin(decl) * self.sin(self.lat)) /
                                     (self.cos(decl) * self.cos(self.lat)))
        return noon + (-t if direction == 'ccw' else t)
    
    def asrTime(self, factor, time):
        """
        Calculate Asr time based on juristic method.
        Shafi: shadow = 1x object, Hanafi: shadow = 2x object.
        """
        
        decl = self.sunPosition(self.jDate + time)[0]
        angle = -self.arccot(factor + self.tan(abs(self.lat - decl)))
        return self.sunAngleTime(angle, time)
    
    def sunPosition(self, jd):
        """
        Calculate sun's declination and equation of time for a given Julian date.
        Based on the U.S. Naval Observatory algorithm.
        """
        
        D = jd - 2451545.0
        g = self.fixangle(357.529 + 0.98560028 * D)
        q = self.fixangle(280.459 + 0.98564736 * D)
        L = self.fixangle(q + 1.915 * self.sin(g) + 0.020 * self.sin(2*g))
        
        e = 23.439 - 0.00000036 * D
        RA = self.arctan2(self.cos(e) * self.sin(L), self.cos(L)) / 15.0
        
        eqt = q/15.0 - self.fixhour(RA) # Equation of time in hours
        decl = self.arcsin(self.sin(e) * self.sin(L)) # Declination of the sun
        
        return (decl, eqt)
    
    def julian(self, year, month, day):
        """Convert Gregorian date to Julian date."""
        
        if month <= 2:
            year -= 1
            month += 12
        A = math.floor(year / 100)
        B = 2 - A + math.floor(A / 4)
        
        JD = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
        return JD
    
    def midDay(self, time):
        """Calculate solar noon (Dhuhr) for the day."""
        
        eqt = self.sunPosition(self.jDate + time)[1]
        noon = self.fixhour(12 - eqt)
        return noon
    
    def dayPortion(self, times):
        """Convert times to fractions of the day (0-1)."""
        
        for i in times:
            times[i] /= 24.0
        return times
    
    def riseSetAngle(self):
        """Standard angle for sunrise/sunset (includes atmospheric refraction)."""
        
        earthRad = 6371009  # in meters
        angle = math.degrees(math.acos(earthRad / (earthRad + 0)))
        return 0.833 + angle
    
    # Trigonometric helper functions (all angles in degrees)
    def sin(self, d): return math.sin(math.radians(d))
    def cos(self, d): return math.cos(math.radians(d))
    def tan(self, d): return math.tan(math.radians(d))
    def arcsin(self, x): return math.degrees(math.asin(x))
    def arccos(self, x): return math.degrees(math.acos(x))
    def arctan(self, x): return math.degrees(math.atan(x))
    def arccot(self, x): return math.degrees(math.atan(1/x))
    def arctan2(self, y, x): return math.degrees(math.atan2(y, x))
    
    def fixangle(self, a):
        """Normalize angle to 0-360 degrees."""
        
        return self.fix(a, 360)
    
    def fixhour(self, a):
        """Normalize hour to 0-24."""
        
        return self.fix(a, 24)
    
    def fix(self, a, b):
        """Normalize value to 0-b."""
        
        a = a - b * math.floor(a / b)
        return a + b if a < 0 else a

def fetch_data():
    """Fetch prayer time data and save to CSV."""
    
    settings = load_settings()
    
    DATA = settings['DATA']
    LATITUDE = DATA['LOCATION']['LATITUDE']
    LONGITUDE = DATA['LOCATION']['LONGITUDE']
    TIMEZONE_NAME = DATA['LOCATION']['TIMEZONE_NAME']
    CALCULATION_METHOD = DATA['CALCULATION']['METHOD']
    JURISTIC_METHOD = DATA['CALCULATION']['JURISTIC_METHOD']
    
    # Initialize
    prayer_times = PrayerTimes(CALCULATION_METHOD)
    prayer_times.setAsrMethod(JURISTIC_METHOD)
    
    header = ["Date", "Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
    rows = []
    
    for i in range(365 * 50): # 50 years
        current_date = datetime.now() + timedelta(days=i)
        dt_with_tz = datetime(current_date.year, current_date.month, current_date.day, 12, 0, tzinfo=ZoneInfo(TIMEZONE_NAME))
        offset = dt_with_tz.utcoffset()
        tz_offset = offset.total_seconds() / 3600 if offset is not None else 0
        times = prayer_times.getTimes(current_date, (LATITUDE, LONGITUDE), tz_offset)
        date_str = current_date.strftime("%d %b %Y")
        
        def float_to_time(t):
            """Convert float hours to 12-hour time format."""
            
            t = t % 24
            hours = int(t)
            minutes = int(round((t - hours) * 60))
            
            # Handle rounding that pushes minutes to 60
            if minutes == 60:
                hours += 1
                minutes = 0
            hours = hours % 24
            
            dt = datetime(current_date.year, current_date.month, current_date.day, hours, minutes, tzinfo=ZoneInfo(TIMEZONE_NAME))
            return dt.strftime("%I:%M %p")
        
        time_list = [
            float_to_time(times['Fajr']),
            float_to_time(times['Sunrise']),
            float_to_time(times['Dhuhr']),
            float_to_time(times['Asr']),
            float_to_time(times['Maghrib']),
            float_to_time(times['Isha'])
        ]
        rows.append([date_str] + time_list)
    
    # Write to CSV file
    with open(CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
        print(f"Prayer times data saved to {CSV}")

if __name__ == "__main__":
    fetch_data()