from praytimes import PrayTimes
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, time

CALCULATION_METHOD = 'ISNA'
LATITUDE = 43.100903
LONGITUDE = -75.232664
TIMEZONE = 'America/New_York'
UTC_OFFSET = -5  # Eastern Time (UTC-5)
ASR_METHOD = 'Hanafi'
FETCH_WINDOW_DAYS = 95

pt = PrayTimes(CALCULATION_METHOD)
pt.adjust({'asr': ASR_METHOD})
pt.adjust({'maghrib': '0 min'})

def format_time(t):
	try:
		return datetime.strptime(t, "%H:%M").strftime("%I:%M %p")
	except Exception:
		return t

print("\nDate,Fajr,Sunrise,Dhuhr,Asr,Maghrib,Isha")

start_date = datetime(2025, 12, 29).date()
for i in range(FETCH_WINDOW_DAYS):
    date_iter = start_date + timedelta(days=i)
    dt_with_time = datetime.combine(date_iter, time(12, 0))
    offset = dt_with_time.astimezone(ZoneInfo(TIMEZONE)).utcoffset()
    tz_offset = int(offset.total_seconds() // 3600) if offset is not None else UTC_OFFSET
    times = pt.getTimes(
        [date_iter.year, date_iter.month, date_iter.day],
        [LATITUDE, LONGITUDE],
        tz_offset
    )
    print(f"{date_iter.strftime('%d %b %Y')},{format_time(times['fajr'])},{format_time(times['sunrise'])},{format_time(times['dhuhr'])},{format_time(times['asr'])},{format_time(times['maghrib'])},{format_time(times['isha'])}")

print("\n")