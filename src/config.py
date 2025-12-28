# config.py

import json

# File paths
CSV_PATH = 'data/prayer_times.csv'
SETTINGS_PATH = 'data/settings.json'
FONT_PATH = 'assets/fonts/BebasNeue-Regular.ttf' # Obtained from https://fonts.google.com/specimen/Bebas+Neue

def load_settings():
    """Load settings from JSON file."""
    with open(SETTINGS_PATH, 'r') as file:
        return json.load(file)

settings = load_settings()

# Main configuration dictionaries
API = settings['API']
DATA = settings['DATA']
DISPLAY = settings['DISPLAY']

HIJRI_MONTH_NAMES = {int(k): v for k, v in DATA['HIJRI_MONTH_NAMES'].items()}

# Display settings
WINDOW = DISPLAY['WINDOW']

FPS = WINDOW['FPS']

PRESET = WINDOW['PRESET']

PRESET_MAP = {
    1: (0, 0, True), # Fullscreen
    2: (1280, 720, False),
    3: (1600, 900, False),
}

WIDTH, HEIGHT, FULLSCREEN = PRESET_MAP[PRESET]

DESIGN_WIDTH, DESIGN_HEIGHT = 1600, 900 # Design dimensions for scaling

NAME = DISPLAY['NAME']
ADDRESS = DISPLAY['ADDRESS']

ANNOUNCEMENTS = DISPLAY.get('ANNOUNCEMENTS', [])

# Color settings
COLORS = DISPLAY['COLORS']

BLACK_COLOR = COLORS['BLACK']
WHITE_COLOR = COLORS['WHITE']
RED_COLOR = COLORS['RED']
NAVY_BLUE_COLOR = COLORS['NAVY_BLUE']
PEACH_COLOR = COLORS['PEACH']

BACKGROUND_COLORS = DISPLAY['BACKGROUND']