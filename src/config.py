# config.py

# File paths
CSV = 'data/data.csv'
SETTINGS = 'data/settings.json'
SETTINGS_TEMPLATE = 'data/settings.template.json'
FONT = 'assets/fonts/Bebas_Neue/BebasNeue-Regular.ttf' # Obtained from https://fonts.google.com/specimen/Bebas+Neue
ARABIC_FONT = 'assets/fonts/UKIJTuzKB.ttf' # Obtained from https://fontlibrary.org/en/font/ukij-tuz
TEXTURE = 'assets/texture.png' # Obtained from https://www.freepik.com/free-vector/abstract-islamic-golden-pattern-backdrop-ethnic-style_297349472.htm
BEEP = 'assets/beep.wav' # Generated using audio.py

PLACEHOLDER = "––––––––––"

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

def rgba(rgb, a):
    """Add alpha to RGB color."""
    
    return rgb + [a]

BLACK = rgb(0,0,0)
WHITE = rgb(255,255,255)
GOLD = rgb(238,198,105)
MIDNIGHT_BLUE = rgb(0,0,39)
ROYAL_BLUE = rgb(0,0,78)