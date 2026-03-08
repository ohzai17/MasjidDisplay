# config.py

import json

# File paths
CSV = 'data/data.csv'
SETTINGS = 'data/settings.json'
FONT = 'assets/fonts/Bebas_Neue/BebasNeue-Regular.ttf' # Obtained from https://fonts.google.com/specimen/Bebas+Neue
ARABIC_FONT = 'assets/fonts/UKIJTuzKB.ttf' # Obtained from https://fontlibrary.org/en/font/ukij-tuz

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

THEMES = [
    {"BACKGROUND": rgb(5, 15, 25), "TEXT": rgb(0, 180, 255)},
    {"BACKGROUND": rgb(5, 25, 15), "TEXT": rgb(0, 255, 120)},
    {"BACKGROUND": rgb(25, 10, 5), "TEXT": rgb(255, 120, 0)},
    {"BACKGROUND": rgb(30, 10, 30), "TEXT": rgb(220, 0, 220)},
    {"BACKGROUND": rgb(10, 30, 30), "TEXT": rgb(0, 220, 220)},
]