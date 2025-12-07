# config.py

import json

CSV_PATH = 'data/prayer_times.csv'
SETTINGS_PATH = 'data/settings.json'
FONT_PATH = 'assets/Bebas-Regular.ttf'

def load_settings():
    """Load settings from JSON file."""
    with open(SETTINGS_PATH, 'r') as file:
        return json.load(file)

settings = load_settings()

# Main dictionaries (shared across project)
API = settings['API']
DATA = settings['DATA']
DISPLAY = settings['DISPLAY']

WINDOW = DISPLAY['WINDOW']
FPS = WINDOW['FPS']
WIDTH = WINDOW['WIDTH']
HEIGHT = WINDOW['HEIGHT']
FULLSCREEN = WINDOW['FULLSCREEN']

COLOR_THEME = DISPLAY['COLOR_THEME']
BACKGROUND_COLOR = COLOR_THEME['BACKGROUND']
PRIMARY_COLOR = COLOR_THEME['PRIMARY']

FONT_SIZE = DISPLAY['FONT']['SIZE']