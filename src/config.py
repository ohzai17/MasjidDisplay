# config.py

import json

# File paths
CSV = 'data/data.csv'
SETTINGS = 'data/settings.json'
FONT = 'assets/fonts/BebasNeue-Regular.ttf' # Obtained from https://fonts.google.com/specimen/Bebas+Neue

def load_settings():
    """Load settings from JSON file."""
    with open(SETTINGS, 'r') as file:
        return json.load(file)

settings = load_settings()

# Display settings
DISPLAY = settings['DISPLAY']

NAME = DISPLAY['NAME']
ADDRESS = DISPLAY['ADDRESS']
ANNOUNCEMENTS = DISPLAY.get('ANNOUNCEMENTS', [])

HIJRI_DATE_ADJUSTMENT = settings.get('HIJRI_DATE_ADJUSTMENT', 0)

# Data settings
DATA = settings['DATA']

LATITUDE = DATA['LOCATION']['LATITUDE']
LONGITUDE = DATA['LOCATION']['LONGITUDE']
TIMEZONE = DATA['LOCATION']['TIMEZONE']['NAME']
UTC_OFFSET = DATA['LOCATION']['TIMEZONE']['UTC_OFFSET']
CALCULATION_METHOD = DATA['CALCULATION']['METHOD']
ASR_METHOD = DATA['CALCULATION']['ASR_METHOD']
ANGLES = DATA['CALCULATION'].get('ANGLES', {})

FETCH_WINDOW = 95
REFRESH_INTERVAL = 90

HIJRI_MONTH_NAMES = {
    1: "Muharram",
    2: "Safar",
    3: "Rabi al-Awwal",
    4: "Rabi al-Thani",
    5: "Jamada al-Awwal",
    6: "Jamada al-Thani",
    7: "Rajab",
    8: "Sha'ban",
    9: "Ramadan",
    10: "Shawwal",
    11: "Dhul-Qadah",
    12: "Dhul-Hijjah"
}

# Window settings
PRESET_MAP = {
    1: (0, 0, True), # Fullscreen
    2: (1280, 720, False),
    3: (1600, 900, False),
}

# Color settings
def rgb(r, g, b):
    """Return RGB color as a list."""
    
    return [r, g, b]

BLACK = rgb(0, 0, 0)
WHITE = rgb(255, 255, 255)
GOLD = rgb(255, 215, 150)

GRADIENTS = {
    "FAJR":     [rgb(20, 35, 65), rgb(10, 15, 30)],
    "SUNRISE":  [rgb(90, 120, 160), rgb(130, 160, 190)],
    "DHUHR":    [rgb(70, 110, 150), rgb(100, 140, 180)],
    "ASR":      [rgb(80, 110, 145), rgb(110, 140, 170)],
    "MAGHRIB":  [rgb(60, 80, 160), rgb(25, 35, 80)],
    "ISHA":     [rgb(35, 50, 85), rgb(8, 12, 20)],
    "NIGHT":    [rgb(15, 25, 45), rgb(30, 45, 65)]
}