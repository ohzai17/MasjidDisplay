# config.py

# File paths
CSV = 'data/data.csv'
SETTINGS = 'data/settings.json'
FONT = 'assets/fonts/Bebas_Neue/BebasNeue-Regular.ttf' # Obtained from https://fonts.google.com/specimen/Bebas+Neue
ARABIC_FONT = 'assets/fonts/UKIJTuzKB.ttf' # Obtained from https://fontlibrary.org/en/font/ukij-tuz

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
def rgb(r,g,b):
    """Return RGB color as a list."""
    
    return [r,g,b]

BLACK = rgb(0,0,0)
WHITE = rgb(255,255,255)

THEMES = [
    {"BACKGROUND": rgb(21,24,27), "TEXT": rgb(139,152,164)},
    {"BACKGROUND": rgb(8,42,25), "TEXT": rgb(84,221,153)},
    {"BACKGROUND": rgb(42,8,25), "TEXT": rgb(221,84,153)},
    {"BACKGROUND": rgb(42,25,8), "TEXT": rgb(221,153,84)},
    {"BACKGROUND": rgb(8,25,42), "TEXT": rgb(84,153,221)}
]