# launcher.py

import os
import csv
import json
import subprocess
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
from src.utils import load_settings
from src.config import CSV, SETTINGS
from tzlocal import get_localzone_name
from zoneinfo import available_timezones

class Launcher(tk.Tk):
    def __init__(self):
        """Initialize the launcher window."""
        
        super().__init__()
        self.geometry("1400x380")
        self.resizable(False, False)
        self.bind("<Escape>", lambda event: self.destroy()) # Temporary: Allow exiting with ESC key
        style = ttk.Style()
        style.configure("Button.TButton", font=("TkDefaultFont", 12, "bold"))
        style.configure("Launch.TButton", font=("TkDefaultFont", 12, "bold"), foreground="red")
        
        self.focus_force() # Temporary: Focus on launcher window
        
        # Main container for frames
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load settings
        self.settings = load_settings()
        
        # Set up frames
        self.setup_left_frame()
        self.setup_middle_frame()
        self.setup_right_frame()
    
    def setup_left_frame(self):
        """Set up the left frame with location and calculation settings."""
        
        # Load settings
        location = self.settings['DATA']['LOCATION']
        calculation = self.settings['DATA']['CALCULATION']
        
        self.left_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(5, 5))
        
        generate_csv_help = (
            "After setting your location and calculation preferences, click 'Generate CSV' to fetch prayer times data.\n"
        )
        
        # Button row in left frame
        self.left_button_frame = ttk.Frame(self.left_frame)
        self.left_button_frame.pack(side="bottom", pady=10)
        generate_csv_btn = ttk.Button(self.left_button_frame, text="Generate CSV", command=self.generate_csv, style="Button.TButton")
        generate_csv_btn.pack(side="left")
        ToolTip(generate_csv_btn, generate_csv_help)
        
        loccal_help = (
            "Set your location, timezone, calculation method, and Asr juristic method for accurate prayer times.\n\n"
            "After entering your settings, click 'Generate CSV' to fetch prayer times data.\n"
        )
        
        title = ttk.Label(self.left_frame, text="Location & Calculation", font=("TkDefaultFont", 12, "bold", "underline"))
        title.pack(side="top", pady=10)
        ToolTip(title, loccal_help)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_entry = ttk.Entry(self.left_frame, textvariable=self.status_var, state="readonly", justify="center")
        self.status_entry.pack(side="bottom", fill="x", padx=10)
        self.update_status()
        
        setting_labels = ["Latitude", "Longitude", "Timezone", "Hijri Date Adjustment", "Calculation Method", "Asr Method"]
        
        timezone_options = sorted(available_timezones())
        hijri_date_adjustment_options = [str(i) for i in range(-1, 2)]
        calculation_method_options = ["MWL", "ISNA", "Egypt", "Makkah", "Karachi", "Tehran", "Jafari", "France", "Russia", "Singapore"]
        asr_method_options = ["Standard (Shafi, Maliki, Hanbali)", "Hanafi"]
        
        # Current settings from JSON (defaults are in place)
        latitude = location.get("LATITUDE", "")
        longitude = location.get("LONGITUDE", "")
        
        # Auto-detect system timezone
        try:
            timezone = get_localzone_name()
        except Exception:
            timezone = ""
        
        timezone = timezone if timezone in timezone_options else location.get("TIMEZONE_NAME", "")
        
        hijri_date_adjustment = location.get("HIJRI_DATE_ADJUSTMENT", 0)
        calculation_method = calculation.get("METHOD", "")
        asr_method = calculation.get("JURISTIC_METHOD", "")
        
        # Settings frame
        settings_frame = ttk.Frame(self.left_frame)
        settings_frame.pack(side="top", fill="x", padx=10, pady=(10, 0))
        
        for row, label in enumerate(setting_labels):
            
            # Labels
            settings_label = ttk.Label(settings_frame, text=label, anchor="w", font=("TkDefaultFont", 12, "bold"))
            settings_label.grid(row=row, column=0, padx=4, pady=2, sticky="w")
            
            latlon_help = (
                "How to find your Latitude and Longitude:\n\n"
                "1. Open Google Maps (https://maps.google.com).\n"
                "2. Search for your masjid or city (e.g., 'Utica, NY').\n"
                "3. Right-click on your masjid or city center.\n"
                "4. Click the coordinates at the top of the menu (e.g., 43.1548, -75.1426) — they will be copied automatically.\n"
                "5. Paste each value into its respective box.\n\n"
                "Tip: For the most accurate times, use your masjid's exact coordinates rather than the city center.\n"
                "Small differences in coordinates don't significantly affect prayer times for locations within the same city.\n"
            )
            
            timezone_help = (
                "Select your timezone from the dropdown menu.\n\n"
                "Your timezone will be auto-detected. Verify it is correct before proceeding.\n"
                "If your city isn't listed, choose the nearest major city in your timezone.\n"
                "For example, New York uses 'America/New_York'.\n\n"
                "If you cannot find your city, search online for '[Your City] IANA timezone'.\n"
            )
            
            hijri_adj_help = (
                "Adjust the Hijri date if your local moon sighting differs from the calculated date.\n\n"
                "Enter -1 to subtract a day, 0 for no adjustment, or +1 to add a day.\n"
            )
            
            calc_method_help = (
                "Choose the calculation method used by your local mosque.\n\n"
                "For example, in North America, the most common methods are ISNA and MWL.\n"
            )
            
            asr_method_help = (
                "Select the Asr juristic method used by your mosque.\n\n"
                "Standard (Shafi, Maliki, Hanbali): Asr begins when the shadow of an object equals its height.\n"
                "Hanafi: Asr begins when the shadow of an object is twice its height.\n"
            )
            
            # Latitude
            if row == 0:
                self.latitude_entry = ttk.Entry(settings_frame, width=25)
                self.latitude_entry.insert(0, latitude)
                self.latitude_entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
                ToolTip(settings_label, latlon_help)
            
            # Longitude
            elif row == 1:
                self.longitude_entry = ttk.Entry(settings_frame, width=25)
                self.longitude_entry.insert(0, longitude)
                self.longitude_entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
                ToolTip(settings_label, latlon_help)
            
            # Timezone
            elif row == 2:
                self.timezone_entry = ttk.Combobox(settings_frame, values=timezone_options, state="readonly", width=25)
                self.timezone_entry.set(timezone)
                self.timezone_entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
                ToolTip(settings_label, timezone_help)
                
            # Hijri Date Adjustment
            elif row == 3:
                self.hijri_date_adjustment_entry = ttk.Combobox(settings_frame, values=hijri_date_adjustment_options, state="readonly", width=25)
                self.hijri_date_adjustment_entry.set(str(hijri_date_adjustment))
                self.hijri_date_adjustment_entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
                ToolTip(settings_label, hijri_adj_help)
            
            # Calculation Method
            elif row == 4:
                self.calculation_method_entry = ttk.Combobox(settings_frame, values=calculation_method_options, state="readonly", width=25)
                self.calculation_method_entry.set(calculation_method)
                self.calculation_method_entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
                ToolTip(settings_label, calc_method_help)
            
            # Asr Method
            elif row == 5:
                self.asr_method_entry = ttk.Combobox(settings_frame, values=asr_method_options, state="readonly", width=25)
                self.asr_method_entry.set(asr_method)
                self.asr_method_entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
                ToolTip(settings_label, asr_method_help)
    
    def setup_middle_frame(self):
        """Set up the middle frame with prayer times table."""
        
        # Load settings
        prayers = self.settings['DATA']['PRAYERS']
        
        self.middle_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.middle_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 5))
        
        restore_defaults_help = (
            "Restore initially loaded settings for the prayer times table.\n"
        )
        
        # Button row in middle frame
        self.middle_button_frame = ttk.Frame(self.middle_frame)
        self.middle_button_frame.pack(side="bottom", pady=10)
        restore_btn = ttk.Button(self.middle_button_frame, text="Restore Defaults", command=self.restore_prayer_defaults, style="Button.TButton")
        restore_btn.pack(side="left")
        ToolTip(restore_btn, restore_defaults_help)
        
        table_help = (
            "Set the fixed Adhan time and Iqamah offset for each prayer.\n\n"
            "Adhan Time: Choose the hour, minute, and AM/PM for the adhan.\n"
            "Iqamah Offset: Enter how many minutes after the adhan the iqamah will be displayed.\n"
            "Clear Button: Delete all fields for that prayer.\n\n"
            "Leave fields blank to use calculated times instead of fixed times.\n"
        )
        
        title = ttk.Label(self.middle_frame, text="Prayer Times Table", font=("TkDefaultFont", 12, "bold", "underline"))
        title.pack(side="top", pady=10)
        ToolTip(title, table_help)
        
        header = ["Prayer", "Hour", "Minute", "AM/PM", "Clear", "Iqamah Offset (min)"]
        self.prayer_labels = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Jummah"]
        
        hours_options = [""] + [f"{i:02d}" for i in range(1, 13)]
        minutes_options = [""] + [f"{i:02d}" for i in range(0, 60, 5)]
        ampm_options = [""] + ["AM", "PM"]
        
        offset_options = [f"{i}" for i in range(0, 31, 5)]
        
        # Table frame
        table_frame = ttk.Frame(self.middle_frame)
        table_frame.pack(side="top", fill="x", padx=10, pady=(10, 0))
        
        # Header row
        for row, label in enumerate(header):
            if label == "Prayer":
                ttk.Label(table_frame, text=label, anchor="w", font=("TkDefaultFont", 12, "bold")).grid(
                    row=0, column=row, padx=4, pady=2, sticky="nsew"
                )
            
            else:
                ttk.Label(table_frame, text=label, anchor="center", font=("TkDefaultFont", 12, "bold")).grid(
                    row=0, column=row, padx=4, pady=2, sticky="nsew"
                )
        
        self.adhan_time_hour_entries = []
        self.adhan_time_minute_entries = []
        self.adhan_time_ampm_entries = []
        self.iqamah_offset_entries = []
        
        # Prayer rows
        for row, label in enumerate(self.prayer_labels, start=1):
            
            # Current settings from JSON (defaults are in place)
            prayer = prayers.get(label.upper(), {})
            adhan_time = prayer.get("ADHAN_TIME", "")
            iqamah_offset = prayer.get("IQAMAH_OFFSET", 0)
            
            hours, minutes, ampm = "", "", ""
            if adhan_time:
                hhmm, ampm = adhan_time.split()
                hours, minutes = hhmm.split(":")
            
            # Prayer Names
            ttk.Label(table_frame, text=label, anchor="w", font=("TkDefaultFont", 12, "bold")).grid(
                row=row, column=0, padx=4, pady=2, sticky="nsew"
            )
            
            # Adhan Time
            hour_entry = ttk.Combobox(table_frame, values=hours_options, state="readonly", width=5)
            hour_entry.set(hours)
            hour_entry.grid(row=row, column=1, padx=4, pady=2, sticky="nsew")
            self.adhan_time_hour_entries.append(hour_entry)
            minute_entry = ttk.Combobox(table_frame, values=minutes_options, state="readonly", width=5)
            minute_entry.set(minutes)
            minute_entry.grid(row=row, column=2, padx=4, pady=2, sticky="nsew")
            self.adhan_time_minute_entries.append(minute_entry)
            ampm_entry = ttk.Combobox(table_frame, values=ampm_options, state="readonly", width=5)
            ampm_entry.set(ampm)
            ampm_entry.grid(row=row, column=3, padx=4, pady=2, sticky="nsew")
            self.adhan_time_ampm_entries.append(ampm_entry)
            
            ttk.Button(table_frame, text="X", width=1,command=lambda i=row-1: self.clear_adhan_time_field(i)
                ).grid(row=row, column=4, padx=4, pady=2, sticky="nsew")
            
            # Iqamah Offset
            iqamah_offset_entry = ttk.Combobox(table_frame, values=offset_options, state="readonly", width=5)
            iqamah_offset_entry.set(iqamah_offset)
            iqamah_offset_entry.grid(row=row, column=5, padx=4, pady=2, sticky="nsew")
            self.iqamah_offset_entries.append(iqamah_offset_entry)
    
    def setup_right_frame(self):
        """Set up the right frame with masjid display information."""
        
        # Load settings
        display = self.settings["DISPLAY"]
        
        self.right_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.right_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 5))
        
        restore_defaults_help = (
            "Restore initially loaded settings for the masjid information.\n"
        )
        
        # Button row in right frame
        self.right_button_frame = ttk.Frame(self.right_frame)
        self.right_button_frame.pack(side="bottom", pady=10)
        restore_btn = ttk.Button(self.right_button_frame, text="Restore Defaults", command=self.restore_display_defaults, style="Button.TButton")
        ToolTip(restore_btn, restore_defaults_help)
        restore_btn.pack(side="left")
        
        masjid_info_help = (
            "Set the display information for your masjid.\n"
        )
        
        title = ttk.Label(self.right_frame, text="Masjid Information", font=("TkDefaultFont", 12, "bold", "underline"))
        title.pack(side="top", pady=10)
        ToolTip(title, masjid_info_help)
        
        announcement_options = [
            "",
            "Eid Al-Fitr Salah: Month DD, YYYY @ HH:MM AM",
            "Eid Al-Adha Salah: Month DD, YYYY @ HH:MM AM"
        ]
        
        # Current settings from JSON (defaults are in place)
        name = display.get("NAME", "")
        address = display.get("ADDRESS", "")
        announcements = display.get("ANNOUNCEMENTS", [])
        
        # Display frame
        display_frame = ttk.Frame(self.right_frame)
        display_frame.pack(side="top", fill="x", padx=10, pady=(10, 0))
        display_frame.columnconfigure(0, weight=1)
        
        name_help = (
            "Enter the name of your masjid.\n"
        )
        
        address_help = (
            "Enter the address of your masjid.\n"
        )
        
        announcement_help = (
            "Set up to 3 custom announcements to display on the screen.\n\n"
            "Press the 'A' key in the main display to toggle announcements on/off.\n"
            "There are pre-formatted options for Eid prayer times.\n\n"
            "Leave fields blank if you do not want to use all announcement slots.\n"
        )
        
        # Masjid Name
        name_label = ttk.Label(display_frame, text="Name", anchor="center", font=("TkDefaultFont", 12, "bold"))
        name_label.grid(row=0, column=0, padx=4, pady=2, sticky="ew")
        ToolTip(name_label, name_help)
        
        self.name_entry = ttk.Entry(display_frame, width=30, justify="center")
        self.name_entry.insert(0, name)
        self.name_entry.grid(row=1, column=0, padx=4, pady=2, sticky="ew")
        
        # Masjid Address
        address_label = ttk.Label(display_frame, text="Address", anchor="center", font=("TkDefaultFont", 12, "bold"))
        address_label.grid(row=2, column=0, padx=4, pady=(8, 2), sticky="ew")
        ToolTip(address_label, address_help)
        
        self.address_entry = ttk.Entry(display_frame, width=30, justify="center")
        self.address_entry.insert(0, address)
        self.address_entry.grid(row=3, column=0, padx=4, pady=2, sticky="ew")
        
        # Announcements
        announcement_label = ttk.Label(display_frame, text="Announcements", anchor="center", font=("TkDefaultFont", 12, "bold"))
        announcement_label.grid(row=4, column=0, padx=4, pady=(8, 2), sticky="ew")
        ToolTip(announcement_label, announcement_help)
        
        self.announcement_entries = []
        for i in range(3):
            announcement_entry = ttk.Combobox(display_frame, values=announcement_options, width=30, justify="center")
            if i < len(announcements):
                announcement_entry.set(announcements[i])
            announcement_entry.grid(row=5 + i, column=0, padx=4, pady=2, sticky="ew")
            self.announcement_entries.append(announcement_entry)
        
        # Configure grid weights for main frame
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=10)
        self.main_frame.rowconfigure(0, weight=1)
        
        launch_info = (
            "Review your settings and click 'Launch' to open the main display.\n\n"
            "If you update any calculation settings, click 'Generate CSV' again to refresh the data before launching.\n"
            "To return to this launcher from the main display, press the 'ESC' key.\n"
        )
        
        # Launch button at the bottom
        launch_btn = ttk.Button(self, text="Launch", style="Launch.TButton", command=self.launch)
        launch_btn.pack(pady=(0, 10))
        ToolTip(launch_btn, launch_info)
    
    def launch(self):
        """Launch the main application."""
        
        if not os.path.exists(CSV):
            messagebox.showerror("Error", "CSV file does not exist. \n\nGenerate before launching.")
            return
        
        if self.save_settings():
            self.destroy()
            subprocess.Popen(["python", "src/main.py"])
    
    def update_status(self):
        """Update the status label."""
        
        if os.path.exists(CSV):
            with open(CSV, newline='') as f:
                rows = list(csv.reader(f))[1:]  # Skip header
                last_date = rows and rows[-1] and rows[-1][0] # Get last date from first column
                self.status_var.set(f"Last date on file: {last_date}")
        
        else:
            self.status_var.set("CSV file does not exist.")
    
    def generate_csv(self):
        """Generate the CSV file."""
        
        from src.data import fetch_data
        
        if self.save_settings():
            try:
                fetch_data()
                self.status_var.set("CSV file generated.")
            except Exception:
                messagebox.showerror("Error", "CSV file failed to generate.\n\n"
                                    "This may be caused by invalid location settings (e.g., latitude or longitude).")
            self.after(1500, self.update_status)
    
    def clear_adhan_time_field(self, i):
        """Clear hour, minute, and AM/PM fields for a specific prayer."""
        
        self.adhan_time_hour_entries[i].set("")
        self.adhan_time_minute_entries[i].set("")
        self.adhan_time_ampm_entries[i].set("")
    
    def restore_prayer_defaults(self):
        """Restore the prayer table fields to initial values."""
        
        prayers = load_settings()['DATA']['PRAYERS']
        
        for i, label in enumerate(self.prayer_labels):
            
            prayer = prayers.get(label.upper(), {})
            adhan_time = prayer.get("ADHAN_TIME", "")
            iqamah_offset = prayer.get("IQAMAH_OFFSET", 0)
            
            hours, minutes, ampm = "", "", ""
            if adhan_time:
                hhmm, ampm = adhan_time.split()
                hours, minutes = hhmm.split(":")
            
            self.adhan_time_hour_entries[i].set(hours)
            self.adhan_time_minute_entries[i].set(minutes)
            self.adhan_time_ampm_entries[i].set(ampm)
            self.iqamah_offset_entries[i].set(iqamah_offset)
    
    def restore_display_defaults(self):
        """Restore the display fields to initial values."""
        
        display = load_settings()['DISPLAY']
        
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, display.get("NAME", ""))
        
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, display.get("ADDRESS", ""))
        
        announcements = display.get("ANNOUNCEMENTS", [])
        for i, entry in enumerate(self.announcement_entries):
            entry.set(announcements[i] if i < len(announcements) else "")
    
    def validate_settings(self):
        """Validate settings before saving."""
        
        # Left frame
        
        timezone = self.timezone_entry.get()
        hijri_date_adjustment = int(self.hijri_date_adjustment_entry.get())
        calculation_method = self.calculation_method_entry.get()
        asr_method = self.asr_method_entry.get()
        
        # Input validation
        try:
            latitude = float(self.latitude_entry.get())
            longitude = float(self.longitude_entry.get())
            
            if not (-90 <= latitude <= 90):
                messagebox.showerror("Error", "Latitude must be between -90 and 90.")
                return False
            
            if not (-180 <= longitude <= 180):
                messagebox.showerror("Error", "Longitude must be between -180 and 180.")
                return False
        
        except ValueError:
            messagebox.showerror("Error", "Latitude and Longitude must be valid numbers.\n\n(e.g., 43.1548, -75.1426)")
            return False
        
        # Right frame
        
        name = self.name_entry.get()
        address = self.address_entry.get()
        announcements = [i.get() for i in self.announcement_entries if i.get()]
        
        # Input validation
        if not name.strip():
            messagebox.showerror("Error", "Masjid Name cannot be empty.")
            return False
        
        if len(name) > 20:
            messagebox.showerror("Error", "Masjid Name exceeds character limit.")
            return False
        
        if not address.strip():
            messagebox.showerror("Error", "Masjid Address cannot be empty.")
            return False
        
        if len(address) > 35:
            messagebox.showerror("Error", "Masjid Address exceeds character limit.")
            return False
        
        for i, announcement in enumerate(announcements):
            if ':' in announcement:
                if len(announcement.strip()) > 45:
                    messagebox.showerror("Error", f"Announcement {i+1} exceeds character limit.")
                    return False
            else:
                if len(announcement.strip()) > 38:
                    messagebox.showerror("Error", f"Announcement {i+1} exceeds character limit.")
                    return False
        
        # Update settings dictionary
        self.settings['DATA']['LOCATION']['LATITUDE'] = latitude
        self.settings['DATA']['LOCATION']['LONGITUDE'] = longitude
        self.settings['DATA']['LOCATION']['TIMEZONE_NAME'] = timezone
        self.settings['DATA']['LOCATION']['HIJRI_DATE_ADJUSTMENT'] = hijri_date_adjustment
        self.settings['DATA']['CALCULATION']['METHOD'] = calculation_method
        self.settings['DATA']['CALCULATION']['JURISTIC_METHOD'] = asr_method
        self.settings['DISPLAY']['NAME'] = name
        self.settings['DISPLAY']['ADDRESS'] = address
        self.settings['DISPLAY']['ANNOUNCEMENTS'] = announcements
        
        # Middle frame
        
        for i, label in enumerate(self.prayer_labels):
            hour = self.adhan_time_hour_entries[i].get()
            minute = self.adhan_time_minute_entries[i].get()
            ampm = self.adhan_time_ampm_entries[i].get()
            iqamah_offset = int(self.iqamah_offset_entries[i].get())
            
            # Compose time string if all parts are selected
            time_str = f"{hour}:{minute} {ampm}" if hour and minute and ampm else None
            
            # Ensure Jummah time is selected before saving
            if label == "Jummah" and not (hour and minute and ampm):
                messagebox.showerror("Error", "Select hour, minute, and AM/PM for Jummah.")
                return False
            
            # Ensure all parts of time are selected before saving
            if (hour and not minute) or (minute and not hour) or ((hour or minute) and not ampm) or (ampm and not (hour and minute)):
                messagebox.showerror("Error", f"Select hour, minute, and AM/PM for {label}.")
                return False
            
            # Ensure that manual data entry is not earlier or later than calculated times in CSV
            if label != "Jummah" and time_str and os.path.exists(CSV):
                with open(CSV, newline='') as f:
                    reader = csv.DictReader(f)
                    today = datetime.now().strftime("%d %b %Y")
                    for row in reader:
                        
                        # Check that manual times are not earlier than calculated times
                        if row["Date"] == today:
                            manual_dt = datetime.strptime(time_str, "%I:%M %p")
                            calc_time = row[label]
                            if calc_time:
                                calc_dt = datetime.strptime(calc_time.strip(), "%I:%M %p")
                                if manual_dt < calc_dt:
                                    messagebox.showerror("Error", f"{label} cannot be earlier than the calculated time. ({calc_time})")
                                    return False
                            
                            # Check that Fajr is not at or after Sunrise
                            if label == "Fajr":
                                sunrise_time = row.get("Sunrise")
                                if sunrise_time:
                                    sunrise_dt = datetime.strptime(sunrise_time.strip(), "%I:%M %p")
                                    if manual_dt > sunrise_dt:
                                        messagebox.showerror("Error", f"Fajr cannot be later than Sunrise. ({sunrise_time})")
                                        return False
                                    if manual_dt == sunrise_dt:
                                        messagebox.showerror("Error", f"Fajr cannot be the same as Sunrise. ({sunrise_time})")
                                        return False
                            
                            # Check against next prayer's calculated time
                            if i < len(self.prayer_labels) - 2:  # Exclude Isha and Jummah
                                next_label = self.prayer_labels[i + 1]
                                next_calc_time = row[next_label]
                                if next_calc_time:
                                    next_calc_dt = datetime.strptime(next_calc_time.strip(), "%I:%M %p")
                                    if manual_dt > next_calc_dt:
                                        messagebox.showerror("Error", f"{label} cannot be later than {next_label}. ({next_calc_time})")
                                        return False
                                    if manual_dt == next_calc_dt:
                                        messagebox.showerror("Error", f"{label} cannot be the same as {next_label}. ({next_calc_time})")
                                        return False
                            
                            break
            
            adhan_time = f"{hour}:{minute} {ampm}" if hour and minute and ampm else ""
            
            # Build prayer dictionary
            prayer_dict = {
                "ADHAN_TIME": adhan_time,
                "IQAMAH_OFFSET": iqamah_offset
            }
            
            # Update settings
            self.settings['DATA']['PRAYERS'][label.upper()] = prayer_dict
        
        return True
    
    def save_settings(self):
        """Save settings to JSON file."""
        
        if not self.validate_settings():
            return False
        
        with open(SETTINGS, "w") as f:
            json.dump(self.settings, f, indent=4)
        
        return True

def ToolTip(widget, text):
    """Create a tooltip for a given widget."""
    
    tipwindow = None
    
    def show_tip(event=None):
        nonlocal tipwindow
        if tipwindow or not text:
            return
        x = widget.winfo_rootx()
        y = widget.winfo_rooty() + 25
        tipwindow = tw = tk.Toplevel(widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=text, justify='left', relief='solid', borderwidth=1)
        label.pack(ipadx=1)
    
    def hide_tip(event=None):
        nonlocal tipwindow
        if tipwindow:
            tipwindow.destroy()
            tipwindow = None
    
    widget.bind("<Enter>", show_tip)
    widget.bind("<Leave>", hide_tip)

if __name__ == "__main__":
    app = Launcher()
    app.mainloop()