# Masjid Display

A local prayer timetable application for masjids, built with Python. It includes a launcher for setup and a live display for daily prayer times.

The screen shows the current time, Gregorian and Hijri dates, masjid name and address, a full prayer table (Adhan and Iqamah) in English and Arabic, a countdown to the next event, and an optional announcement panel.

---

## Demo

![Demo](assets/demo.gif)

---

## Requirements

| Requirement | Details |
|-------------|---------|
| **Python** | `3.12.x` (tested on `3.12.3`) |
| **OS** | macOS or Windows with display and audio support |

> Linux is untested and not officially supported.

---

## Installation

```bash
# 1. Open the project root
cd /path/to/MasjidDisplay

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate it
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\Activate.ps1       # Windows PowerShell
.venv\Scripts\activate.bat       # Windows Command Prompt

# 4. Install dependencies
pip install -r requirements.txt
```

---

## First-Time Setup

```bash
python -m src.launcher
```

Complete the following steps in order:

| Step | Action |
|------|--------|
| 1 | Enter **Latitude** and **Longitude** for your masjid |
| 2 | Select your **Timezone**, **Calculation Method**, and **Asr Method** |
| 3 | Click **Generate CSV** — creates `data/data.csv` covering ~10 years |
| 4 | Enter the **Masjid Name** and **Address** |
| 5 | Set the **Jummah** time (hour, minute, AM/PM) |
| 6 | Click **Launch** |

> See the [Launcher Configuration Guide](#launcher-configuration-guide) for detailed guidance on each field.

---

## Daily Use


### Launch

| Command | Description |
|---------|-------------|
| `python -m src.launcher` | Open the launcher (recommended) |
| `python -m src.main` | Launch the display directly, skipping the launcher |

> Without a valid CSV, the display falls back to placeholder values.


### Update Settings While the Display is Running

1. Press `ESC` or close the window (`X`) to return to the launcher
2. Make your changes
3. Click **Generate CSV** if you changed the location, timezone, calculation method, or Asr method
4. Click **Launch** to restart the display

> Skipping **Generate CSV** after a location or method change will cause the display to use outdated prayer times.


### Regenerate the CSV

Regenerate whenever you change any of the following:

- Location (latitude or longitude)
- Timezone
- Calculation method
- Asr method


### Close the Display

Press `ESC` or click the window's close button (`X`) to exit and return to the launcher.

---

## Launcher Configuration Guide


### Location and Timezone

**Finding your coordinates:**

1. Open [Google Maps](https://maps.google.com)
2. Search for your masjid or city (e.g., "Utica, NY")
3. Right-click your exact location
4. Click the coordinates at the top of the context menu — they copy automatically
5. Paste each value into the Latitude and Longitude fields

> Using the masjid's exact coordinates gives the most accurate prayer times. Small differences within the same city have minimal impact.

**Timezone:** Select from the dropdown in IANA format (e.g., `America/New_York`, `Europe/London`). Your system timezone is auto-detected when available — verify it before proceeding.

**Hijri Date Adjustment:** If your local moon sighting differs from the calculated date, offset by `-1`, `0`, or `+1` days.


### Calculation and Asr Methods

**Calculation Method:** Choose the method your masjid follows. Common choices for North America are **ISNA** and **MWL**.

Supported methods: `MWL` `ISNA` `Egypt` `Makkah` `Karachi` `Tehran` `Jafari` `France` `Russia` `Singapore`

**Asr Juristic Method:**

| Method | Rule |
|--------|------|
| Standard (Shafi, Maliki, Hanbali) | Shadow length = object height |
| Hanafi | Shadow length = 2× object height |


### Prayer Time Overrides

**Adhan Time:** Optionally set a fixed adhan time per prayer. Leave blank to use calculated times from the CSV. Select hour (1–12), minute (5-minute increments), and AM/PM — all three fields must be set together. For non-Jummah prayers, the override cannot be earlier than the calculated time.

**Iqamah Offset:** Minutes after Adhan the Iqamah is announced — `0`, `5`, `10`, `15`, `20`, or `30`.

**Jummah:** A fixed adhan time is required and must fall between `11:00 AM` and `3:00 PM`.


### Masjid Information

| Field | Limit | Notes |
|-------|-------|-------|
| Name | 20 characters | Required |
| Address | 35 characters | Leave blank if unused |
| Announcements | 45 characters each | Up to 3 messages; toggle with `A` |

Pre-formatted announcement templates are available:
- `Eid Al-Fitr Salah: Month DD, YYYY @ HH:MM AM`
- `Eid Al-Adha Salah: Month DD, YYYY @ HH:MM AM`

---

## Keyboard Controls

| Key | Action |
|-----|--------|
| `ESC` | Exit display and reopen launcher |
| `X` | Exit display and reopen launcher |
| `1` | Fullscreen (startup default) |
| `2` | 1280×720 windowed |
| `3` | 1600×900 windowed |
| `A` | Toggle announcements panel |

---

## How It Works


### Prayer Time Calculation

Prayer times are calculated using astronomical formulas derived from [PrayTimes.org](https://praytimes.org/docs/calculation) and saved to `data/data.csv` covering approximately 10 years from the current date.

| Prayer | Calculation Method |
|--------|--------------------|
| Fajr / Isha | Sun angle below the horizon (method-specific) |
| Sunrise / Sunset | Atmospheric refraction adjustment (0.833°) |
| Dhuhr | Solar noon (equation of time) |
| Asr | Sun angle — Standard or Hanafi |
| Maghrib | Sunset (solar noon + declination adjustment) |

The engine handles Julian date conversion, solar declination and equation of time, trigonometric sun angle computations, and timezone/longitude adjustments for local accuracy.


### Launcher

The launcher manages configuration, validation, and CSV generation. It handles per-prayer Adhan overrides, Iqamah offsets, masjid identity, and announcement messages. It auto-detects the local timezone and validates all input before saving to `data/settings.json`.


### Live Display

The Pygame display renders the live clock, Gregorian and Hijri dates, the prayer table, and the next-event countdown.

Notable behaviors:
- The next upcoming prayer or event is highlighted in the table
- On Fridays, Dhuhr is replaced with Jummah
- The Hijri date advances after Maghrib
- A beep plays when the countdown reaches zero
- After all daily events pass, the countdown targets tomorrow's Fajr
- If no valid CSV data exists for today, a fallback view is shown with placeholder values

---

## Project Structure

```
MasjidDisplay/
├── LICENSE
├── requirements.txt
├── README.md
├── assets/
│   ├── fonts/
│   │   ├── UKIJTuzKB.ttf
│   │   └── Bebas_Neue/
│   │       └── BebasNeue-Regular.ttf
│   ├── demo.gif
│   ├── beep.wav
│   └── texture.png
├── data/
│   ├── data.csv
│   └── settings.json
└── src/
    ├── launcher.py
    ├── main.py
    ├── data.py
    ├── config.py
    ├── utils.py
    ├── audio.py
    └── features/
        ├── background.py
        ├── display.py
        ├── table.py
        ├── countdown.py
        └── announcements.py
```

---

## Settings Reference

All settings are stored in `data/settings.json`.

| Section | Key | Description |
|---------|-----|-------------|
| `DISPLAY` | `NAME` | Masjid name |
| `DISPLAY` | `ADDRESS` | Masjid address |
| `DISPLAY` | `ANNOUNCEMENTS` | List of up to 3 messages |
| `DATA.LOCATION` | `LATITUDE` | Decimal latitude |
| `DATA.LOCATION` | `LONGITUDE` | Decimal longitude |
| `DATA.LOCATION` | `TIMEZONE_NAME` | IANA timezone string |
| `DATA.LOCATION` | `HIJRI_DATE_ADJUSTMENT` | `-1`, `0`, or `1` |
| `DATA.CALCULATION` | `METHOD` | Prayer calculation method |
| `DATA.CALCULATION` | `JURISTIC_METHOD` | Asr juristic method |
| `DATA.PRAYERS` | `ADHAN_TIME` | Optional manual time (`HH:MM AM/PM`); required for Jummah |
| `DATA.PRAYERS` | `IQAMAH_OFFSET` | Minutes after adhan |

Per-prayer keys apply to: `FAJR` `DHUHR` `ASR` `MAGHRIB` `ISHA` `JUMMAH`

> To reset all settings to defaults, delete `data/settings.json` and relaunch — defaults are recreated automatically.

---

## Validation Rules

| Field | Rule |
|-------|------|
| Latitude | Between `-90` and `90` |
| Longitude | Between `-180` and `180` |
| Timezone / Calculation / Asr Method | Cannot be empty |
| Masjid Name | Required, max 20 characters |
| Address | Max 35 characters |
| Announcements | Max 45 characters each |
| Prayer Time Entry | Hour, minute, and AM/PM must all be set together |
| Jummah | Between `11:00 AM` and `3:00 PM`; all three fields required |
| Launch | Blocked if `data/data.csv` is missing or outdated |

---

## Troubleshooting

**Display fails to start**
- Confirm these files exist: `assets/texture.png`, `assets/fonts/Bebas_Neue/BebasNeue-Regular.ttf`, `assets/fonts/UKIJTuzKB.ttf`
- Relaunch `python -m src.launcher` and verify all settings

**CSV is missing**
- The CSV has never been generated for your current configuration
- Open the launcher and click **Generate CSV**

**CSV is outdated**
- The CSV no longer covers today's date, or settings have changed since it was last generated
- Click **Generate CSV** again to refresh

**CSV generation fails**
- Most commonly caused by invalid coordinates (including edge cases like exactly ±90 or ±180), a non-numeric value in either field, or an unrecognized timezone
- Verify all three before retrying

**Display shows placeholder values**
- Today's date is not present in `data/data.csv`
- Regenerate the CSV from the launcher

**No beep at zero seconds**
- Check your system volume and audio output device
- Confirm `assets/beep.wav` exists

**Settings appear incorrect after an update**
- The settings schema may have changed — your existing `data/settings.json` could be stale
- Delete it and reconfigure from the launcher; defaults are recreated automatically

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `pygame` | Live display rendering and audio |
| `numpy` | Beep generation (`src/audio.py`) |
| `hijridate` | Hijri calendar conversion |
| `tzlocal` | Local timezone detection |
| `arabic_reshaper` | Arabic text shaping |
| `python-bidi` | Right-to-left text rendering |
| `sv_ttk` | Launcher UI theming |

See [requirements.txt](requirements.txt) for pinned versions.

---

## Assets and Attribution

| Asset | Source | License |
|-------|--------|---------|
| `assets/texture.png` | [Freepik](https://www.freepik.com/free-vector/abstract-islamic-golden-pattern-backdrop-ethnic-style_297349472.htm) | Freepik License |
| `assets/beep.wav` | Generated locally via [src/audio.py](src/audio.py) | — |
| `assets/fonts/Bebas_Neue/BebasNeue-Regular.ttf` | [Google Fonts](https://fonts.google.com/specimen/Bebas+Neue) | SIL OFL 1.1 |
| `assets/fonts/UKIJTuzKB.ttf` | [Font Library](https://fontlibrary.org/en/font/ukij-tuz) | SIL OFL 1.1 |

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.