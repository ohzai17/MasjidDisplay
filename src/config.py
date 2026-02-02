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
ANNOUNCEMENTS = DISPLAY['ANNOUNCEMENTS']

# Data settings
DATA = settings['DATA']

LATITUDE = DATA['LOCATION']['LATITUDE']
LONGITUDE = DATA['LOCATION']['LONGITUDE']
TIMEZONE = DATA['LOCATION']['TIMEZONE']

HIJRI_DATE_ADJUSTMENT = DATA['LOCATION']['HIJRI_DATE_ADJUSTMENT']

CALCULATION_METHOD = DATA['CALCULATION']['METHOD']
ASR_METHOD = DATA['CALCULATION']['ASR_METHOD']

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
    "FAJR":     [rgb(25, 40, 65), rgb(30, 45, 75)],
    "SUNRISE":  [rgb(30, 45, 75), rgb(45, 70, 120)],
    "DHUHR":    [rgb(30, 45, 75), rgb(45, 70, 120)],
    "ASR":      [rgb(30, 45, 75), rgb(45, 70, 120)],
    "MAGHRIB":  [rgb(30, 45, 75), rgb(45, 70, 120)],
    "ISHA":     [rgb(30, 45, 75), rgb(45, 70, 120)],
    "NIGHT":    [rgb(25, 40, 65), rgb(30, 45, 75)]
}