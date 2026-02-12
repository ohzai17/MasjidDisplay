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

GRADIENTS = {key: [rgb(25, 40, 65), rgb(30, 45, 75)] for key in [
    "FAJR", "SUNRISE", "DHUHR", "ASR", "MAGHRIB", "ISHA", "NIGHT"
]}