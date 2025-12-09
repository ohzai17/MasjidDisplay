# config.py

import json

# File paths
CSV_PATH = 'data/prayer_times.csv'
SETTINGS_PATH = 'data/settings.json'
FONT_PATH = 'assets/BebasNeue-Regular.ttf' # Obtained from https://fonts.google.com/specimen/Bebas+Neue

def load_settings():
    """Load settings from JSON file."""
    with open(SETTINGS_PATH, 'r') as file:
        return json.load(file)

settings = load_settings()

# Main configuration dictionaries
API = settings['API']
DATA = settings['DATA']
DISPLAY = settings['DISPLAY']

# Display settings
WINDOW = DISPLAY['WINDOW']

FPS = WINDOW['FPS']
WIDTH = WINDOW['WIDTH']
HEIGHT = WINDOW['HEIGHT']
FULLSCREEN = WINDOW['FULLSCREEN']

NAME = DISPLAY['NAME']
ADDRESS = DISPLAY['ADDRESS']

ANNOUNCEMENTS = DISPLAY.get('ANNOUNCEMENTS', [])

# Color settings
COLORS = DISPLAY['COLORS']

BACKGROUND_COLOR = COLORS['BACKGROUND']
BLACK_COLOR = COLORS['BLACK']
WHITE_COLOR = COLORS['WHITE']
HIGHLIGHT_COLOR = COLORS['HIGHLIGHT']

# Hijri month names
HIJRI_MONTH_NAMES = {
    1: "Muharram", 2: "Safar", 3: "Rabi al-Awwal", 4: "Rabi al-Thani",
    5: "Jamada al-Awwal", 6: "Jamada al-Thani", 7: "Rajab", 8: "Sha'ban",
    9: "Ramadan", 10: "Shawwal", 11: "Dhul-Qadah", 12: "Dhul-Hijjah"
}