# Masjid Display

**Masjid Display** is a local prayer timetable application for masjids, built with Python to deliver a bold, always-on screen experience.

It combines:

- **A launcher UI** (Tkinter) for configuration and validation
- **A long-range dataset** (CSV) for prayer timetable generation
- **A live display UI** (Pygame) for daily operation

The app is designed to run continuously on a display machine and show:

- Current time and Gregorian/Hijri dates
- Masjid name and address
- Prayer table (Adhan and Iqamah)
- Countdown to the next event
- Optional announcement panel

## How It Works

### 1. Prayer Time Calculation and CSV Generation

The app calculates prayer times using astronomical formulas largely derived from [PrayTimes.org](https://praytimes.org/docs/calculation). It generates `data/data.csv` for approximately 10 years from the current date.

**Prayer Time Calculation Engine**

The `PrayerTimes` class in [src/data.py](src/data.py) implements precise astronomical calculations:

- **Fajr** and **Isha**: Calculated based on the sun's angle below the horizon (method-specific)
- **Sunrise** and **Sunset**: Calculated with atmospheric refraction adjustment (0.833°)
- **Dhuhr**: Based on solar noon (using the equation of time)
- **Asr**: Calculated using the sun's angle, with support for two juristic schools:
  - **Standard (Shafi, Maliki, Hanbali)**: Shadow length = object height
  - **Hanafi**: Shadow length = 2 × object height
- **Maghrib**: Set to sunset time (solar noon + declination adjustment)

**Engine Mechanisms:**

- Julian date conversion for astronomical accuracy
- Solar declination and equation of time calculations
- Trigonometric functions for sun angle computations
- Timezone and longitude adjustments for local accuracy

**Supported calculation methods:**

- `MWL`
- `ISNA`
- `Egypt`
- `Makkah`
- `Karachi`
- `Tehran`
- `Jafari`
- `France`
- `Russia`
- `Singapore`

**Supported Asr juristic methods:**

- `Standard (Shafi, Maliki, Hanbali)`
- `Hanafi`

### 2. Launcher (Configuration UI)

The launcher is the control center for all settings. It allows you to configure:

- Location and calculation settings
- Per-prayer Adhan manual override times
- Per-prayer Iqamah offsets
- Masjid display identity (name/address)
- Up to 3 announcements

**Automated Features:**

- Auto-detects local timezone (when available)
- Validates all user input before saving
- Detects whether CSV is missing or outdated
- Prevents launching the display if CSV is invalid

### 3. Live Display (Main Screen)

The Pygame display renders:

- Digital clock
- Gregorian date
- Hijri date (with configurable day adjustment)
- Prayer table in English and Arabic
- Next event countdown (Adhan/Iqamah/Sunrise)

**Behavioral Notes:**

- If no valid prayer data exists for today, placeholders are shown.
- Text color scheme changes based on data availability.
- A beep sound is played when the countdown reaches zero.
- On Fridays, countdown logic uses `Jummah` instead of `Dhuhr`.
- After all today's prayers have passed, the display shows a countdown to tomorrow's Fajr using today's prayer schedule.

## Project Structure

```text
MasjidDisplay/
├── LICENSE
├── requirements.txt
├── README.md
├── assets/
│   ├── fonts/
│   │   ├── UKIJTuzKB.ttf
│   │   └── Bebas_Neue/
│   │       └── BebasNeue-Regular.ttf
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

## Requirements

- Python `3.12.x` (project dependencies tested on Python `3.12.3`)
- macOS with display/audio support
- Windows with display/audio support

*Linux may work, but it is not officially tested*

## Version

- Current app version: `1.0.0` (defined in `src/__init__.py`)

## Release Notes

### 1.0.0

- Initial public release.

## Future Plans

The next phase is an attendee-focused web page (mobile and desktop) that displays the current date and Hijri date, a live clock, all five daily prayers plus Jummah with Adhan and Iqamah times, and a countdown to the next event.

## Setup

### 1. Create and Activate Virtual Environment

Using `venv` is recommended to isolate project dependencies.

```bash
# Create virtual environment
python -m venv .venv

# Activate (macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Settings File Setup

**The template file must be present as part of the application package.**

On first run, the app creates settings from the template:

- `data/settings.template.json` — default template (part of package, must be present)
- `data/settings.json` — active settings file, created from template on first run

If `data/settings.json` is missing or malformed, the app automatically recreates it from `data/settings.template.json`.

## How To Run

**Recommended: run the launcher first.**

**Run the launcher:**

```bash
python -m src.launcher
```

**Recommended first-time workflow:**

1. Enter Masjid information (**Name** and **Address**).
2. Enter valid **Latitude/Longitude** and select **Timezone**, **Calculation Method**, and **Asr Method**.
3. Click **Generate CSV**.
4. Set the **Jummah** time (hour, minute, and AM/PM).
5. Click **Launch**.

*Note: If `data/data.csv` is not found, launch is blocked and you must generate CSV first.*

**Closing the display:**

Press `ESC` or close the window (`X`) to close the display and reopen the launcher.

**Run the display directly:**

```bash
python -m src.main
```

*Note: Direct display launch is supported, but launcher-first is the intended workflow for setup and validation. The display can open without a valid CSV, but prayer/event data will fall back to placeholders until `data/data.csv` is generated and current.*

## Demo

Below is a typical Masjid Display workflow:

![Demo](assets/demo.gif)

## Launcher Configuration Guide

### Location and Timezone

**Latitude and Longitude**

1. Open [Google Maps](https://maps.google.com)
2. Search for your Masjid or city (e.g., "Utica, NY")
3. Right-click on your Masjid or city center
4. Click the coordinates at the top of the menu (e.g., 43.1548, -75.1426) — they will be copied automatically
5. Paste each value into its respective field

*Tip: For the most accurate times, use your Masjid's exact coordinates rather than the city center. Small differences in coordinates don't significantly affect prayer times for locations within the same city.*

**Timezone**

Select your timezone from the dropdown menu (IANA format, e.g., `America/New_York`, `Europe/London`). Your system timezone will be auto-detected when available—verify it is correct before proceeding.

### Adjustments & Methods

- **Hijri Date Adjustment:** 
  Adjust the Hijri date if your local moon sighting differs from the calculated date:
  - `-1`: Subtract one day
  - `0`: No adjustment (default)
  - `+1`: Add one day

- **Calculation Method:**
  Choose the calculation method used by your local masjid (e.g., **ISNA** or **MWL** in North America).

- **Asr Juristic Method**
  Select the Asr juristic method used by your local masjid:
  - **Standard (Shafi, Maliki, Hanbali)**: Asr begins when the shadow of an object equals its height.
  - **Hanafi**: Asr begins when the shadow of an object is twice its height.

### Prayer Time Overrides

**Adhan Time**

Optionally set a fixed adhan time for each prayer. Leave blank to use calculated times from the CSV.

- Select **hour** (1–12), **minute** (in 5-minute increments), and **AM/PM**.
- All three fields must be completed together.
- For non-Jummah prayers, the override **cannot** be earlier than the calculated time.

**Iqamah Offset**

Set how many minutes after Adhan the Iqamah will be announced.

**Jummah (Friday Prayer)**

- Adhan time is **required** and must be between `11:00 AM` and `3:00 PM`

**Masjid Information**

- **Name:** Enter the name of your Masjid (20 characters max).

- **Address:** Enter the address of your Masjid (35 characters max). Leave blank if unused.

- **Announcements:** Set up to 3 custom announcements to display on the screen (45 characters max). Press `A` in the display to toggle the announcement panel. Leave blank if unused.

  Pre-formatted options are available for Eid prayer times:
  - `Eid Al-Fitr Salah: Month DD, YYYY @ HH:MM AM`
  - `Eid Al-Adha Salah: Month DD, YYYY @ HH:MM AM`

## Keyboard Controls (Display)

- `ESC`: Exit display and reopen launcher
- `Window close (X)`: Close display and reopen launcher
- `1`: Fullscreen preset (startup default)
- `2`: 1280x720 window preset
- `3`: 1600x900 window preset
- `A`: Toggle announcements panel

## Feature Overview

### Launcher features

- **Masjid Information:** Supports Masjid name, address, and announcement configuration.
- **Location & Methods:** Supports latitude/longitude, timezone, calculation method, Asr method, and Hijri date adjustment.
- **Prayer Configuration:** Supports manual prayer time input, per-row clear actions, and Iqamah offsets.

- **Restore Defaults:** Only restores initially loaded Masjid Information fields (Name, Address, Announcements). It does **not** reset location, calculation, or timetables.
- **Clearing Rows:** Each prayer row has an **X** button that clears Hour, Minute, and AM/PM together.
- **Iqamah Offsets:** Fixed options only (`0`, `5`, `10`, `15`, `20`, `30` minutes).
- **CSV Generation:** Validates and saves current settings before generating. Applies the selected IANA timezone with per-day UTC offset handling (DST changes are reflected).
- **Status Indicators:** Shows either the CSV last date on file or an outdated/missing CSV message. The file is outdated when the final date is earlier than today.

### Display features

- **Daily Time Updates:** Clock and date update continuously during runtime.
- **Next Prayer Highlighting:** Table highlights the upcoming prayer/event.
- **Friday Behavior:** Dhuhr is replaced with Jummah on Fridays.

- **Fallback View:** Switches to a fallback view (white background) if no valid prayer data exists for today.

- **Audio Beep:** Triggered when the countdown reaches zero.

- **Countdown:** Shows one dominant unit at a time (`Hours`, `Minutes`, or `Seconds`). Targets next day's Fajr if all daily events pass.

- **Announcements:** Hidden by default on startup and toggled with `A`.

- **Announcement Formatting:** Applies display-side truncation for long lines. Text before `:` is highlighted. Text after `:` is truncated to 26 characters. If no `:` is present, the line is truncated to 38 characters.

- **Translations:** English/Arabic prayer labels render side by side.

- **Hijri Date:** Advances after Maghrib for the displayed Islamic date, then applies user adjustment.

### Data generation features

- **Long-Range Generation:** Generates daily prayer data from today through approximately 10 years ahead.
- **Method-Based Calculation:** Uses the selected calculation method and Asr juristic method when building rows.
- **Timezone and DST Handling:** Applies the selected IANA timezone with per-day UTC offset handling so DST changes are reflected in generated rows.
- **Structured CSV Output:** Writes a consistent CSV schema (`Date`, `Fajr`, `Sunrise`, `Dhuhr`, `Asr`, `Maghrib`, `Isha`) for display/runtime consumption.
- **Regeneration Behavior:** Re-generating CSV overwrites the existing file with refreshed future data.

## Settings Overview (data/settings.json)

### DISPLAY

- `NAME`: Masjid name
- `ADDRESS`: Masjid address
- `ANNOUNCEMENTS`: List of up to 3 short messages

### DATA.LOCATION

- `LATITUDE`: Decimal latitude
- `LONGITUDE`: Decimal longitude
- `TIMEZONE_NAME`: IANA timezone
- `HIJRI_DATE_ADJUSTMENT`: `-1`, `0`, or `1`

### DATA.CALCULATION

- `METHOD`: Prayer calculation method name
- `JURISTIC_METHOD`: Asr juristic method

### DATA.PRAYERS

Per prayer (`FAJR`, `DHUHR`, `ASR`, `MAGHRIB`, `ISHA`, `JUMMAH`):

- `ADHAN_TIME`: Optional manual time in `HH:MM AM/PM` (required for `JUMMAH`)
- `IQAMAH_OFFSET`: Minutes after adhan

## Launcher Validation Rules

- **Launch Prerequisite:** Launch is blocked if `data/data.csv` is not found.

- **Location:**
  - **Latitude:** Must be between `-90` and `90`.
  - **Longitude:** Must be between `-180` and `180`.
  - **Latitude** and **longitude** must be valid numbers (for example, `43.1548, -75.1426`).

- **Required Selections:** **Timezone**, **calculation method**, and **Asr method** cannot be empty.

- **Masjid Information:**
  - **Name:** Cannot be empty and is capped at 20 characters.
  - **Address:** Capped at 35 characters.
  - **Announcement:** Capped at 45 characters.

- **Prayer Time Entry:**
  - Partial manual time input is rejected (**hour**/**minute**/**AM/PM** must all be present).
  - Manual prayer times are checked against calculated values to avoid invalid ordering.
  - **Jummah:** 
    - Must be set between `11:00 AM` and `3:00 PM`.
    - **Hour**, **minute**, and **AM/PM** are required.

## Display Logic Notes

- **Hijri Date Rollover:** Hijri date advances after Maghrib for the displayed Islamic date, then applies user adjustment.
- **Next-Day Countdown:** If all daily events pass, countdown targets next day's Fajr using today's loaded Fajr value.
- **Bilingual Labels:** English/Arabic prayer labels are rendered side by side.
- **Background State:** Background style changes depending on whether data is available.

## Data Files

- **Settings File (`data/settings.json`):** Persistent app settings managed by launcher.
- **Settings Template (`data/settings.template.json`):** Default schema template included in the app package.
- **Timetable File (`data/data.csv`):** Generated timetable used by the display.

**Regenerate CSV After Changing:**
- Latitude/longitude
- Timezone
- Calculation method
- Asr juristic method

## Troubleshooting

- **Display Fails to Start:**
  - Confirm required assets exist: `assets/texture.png`, `assets/fonts/Bebas_Neue/BebasNeue-Regular.ttf`, `assets/fonts/UKIJTuzKB.ttf`.
  - If display startup fails, relaunch `python -m src.launcher` and verify settings/paths.

- **CSV Missing:** Open launcher and click **Generate CSV**.

- **CSV Outdated:** Click **Generate CSV** again to refresh future dates.

- **CSV Generation Failed:**
  - Most commonly caused by incorrect location input (latitude/longitude), including edge-case values (such as ±90 latitude or ±180 longitude) that may not work properly in calculations.
  - Check latitude/longitude formatting and ensure both values are numeric.
  - Ensure timezone is valid.

- **Display Shows Placeholders:**
  - Confirm today's date is present in `data/data.csv`.
  - Regenerate CSV from launcher.

- **No Beep at Zero Seconds:**
  - Check system volume and output device.
  - Confirm `assets/beep.wav` exists.

- **Reset Settings to Defaults:**
  - Delete `data/settings.json`.
  - Launch the app again; defaults and template are recreated automatically.

## Dependencies

The project currently uses:

- `pygame`
- `numpy`
- `hijridate`
- `tzlocal`
- `arabic_reshaper`
- `python-bidi`
- `sv_ttk`

See [requirements.txt](requirements.txt) for pinned versions.

## Assets and Attribution

This project uses the following external assets:

- **Texture Background:** Used for `assets/texture.png`. Sourced from [Freepik](https://www.freepik.com/free-vector/abstract-islamic-golden-pattern-backdrop-ethnic-style_297349472.htm) and licensed under the **Freepik License**.
- **Beep Sound:** Used for `assets/beep.wav`. Generated locally using [src/audio.py](src/audio.py).
- **Bebas Neue Font:** Used for `assets/fonts/Bebas_Neue/BebasNeue-Regular.ttf`. Sourced from [Google Fonts](https://fonts.google.com/specimen/Bebas+Neue) and licensed under the **SIL Open Font License 1.1 (OFL)**.
- **Arabic Font (UKIJ Tuz):** Used for `assets/fonts/UKIJTuzKB.ttf`. Sourced from [Font Library](https://fontlibrary.org/en/font/ukij-tuz) and licensed under the **SIL Open Font License 1.1 (OFL)**.

Source links are also documented inline in `src/config.py` comments for quick code-level attribution reference.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.