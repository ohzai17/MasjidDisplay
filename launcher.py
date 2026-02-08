import os
import csv
import json
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from zoneinfo import available_timezones

SETTINGS = 'data/settings.json'
CSV = 'data/data.csv'

class Launcher(tk.Tk):
    def __init__(self):
        
        super().__init__()
        self.geometry("1350x400")
        self.resizable(False, False)
        style = ttk.Style()
        style.configure("Launch.TButton", font=("TkDefaultFont", 12, "bold"))
        
        self.focus_force() # Temporary: Focus on launcher window
        
        # Main container for frames
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load settings
        self.settings = load_settings()
        display = self.settings["DISPLAY"]
        location = self.settings['DATA']['LOCATION']
        calculation = self.settings['DATA']['CALCULATION']
        prayers = self.settings['DATA']['PRAYERS']
        
        # Left frame
        self.left_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Button row in left frame
        self.left_button_frame = ttk.Frame(self.left_frame)
        self.left_button_frame.pack(side="bottom", pady=10)
        ttk.Button(self.left_button_frame, text="Generate CSV", command=self.generate_csv).pack(side="left")
        ttk.Button(self.left_button_frame, text="Delete CSV", command=self.delete_csv).pack(side="left", padx=10)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_entry = ttk.Entry(self.left_frame, textvariable=self.status_var, state="readonly", justify="center")
        self.status_entry.pack(side="bottom", fill="x", padx=10)
        self.update_status()
        
        setting_labels = ["Latitude", "Longitude", "Timezone", "Hijri Date Adjustment", "Calculation Method", "Asr Method"]
        
        timezone_options = sorted(available_timezones())
        hijri_date_adjustment_options = [f"{i}" for i in range(-1, 2)]
        calculation_method_options = ["MWL", "ISNA", "Egypt", "Makkah", "Karachi", "Tehran", "Jafari", "France", "Russia", "Singapore"]
        asr_method_options = ["Standard (Shafi, Maliki, Hanbali)", "Hanafi"]
        
        # Current settings from JSON (defaults are in place)
        latitude = location.get("LATITUDE", "")
        longitude = location.get("LONGITUDE", "")
        timezone = location.get("TIMEZONE_NAME", "")
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
            
            coord_help = (
                "To find your Latitude and Longitude:\n\n"
                "1. Open Google Maps (https://maps.google.com)\n"
                "2. Search for your location or navigate to it manually.\n"
                "3. Right-click your location.\n"
                "4. The coordinates (latitude, longitude) appear at the top of the menu — click to copy.\t\n"
                "5. Enter each value in its respective box.\n"
            )
            
            # Latitude
            if row == 0:
                self.latitude_entry = ttk.Entry(settings_frame, width=25)
                self.latitude_entry.insert(0, latitude)
                self.latitude_entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
                ToolTip(settings_label, coord_help)
            
            # Longitude
            elif row == 1:
                self.longitude_entry = ttk.Entry(settings_frame, width=25)
                self.longitude_entry.insert(0, longitude)
                self.longitude_entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
                ToolTip(settings_label, coord_help)
            
            # Timezone
            elif row == 2:
                self.timezone_entry = ttk.Combobox(settings_frame, values=timezone_options, state="readonly", width=25)
                self.timezone_entry.set(timezone)
                self.timezone_entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
            
            # Hijri Date Adjustment
            elif row == 3:
                self.hijri_date_adjustment_entry = ttk.Combobox(settings_frame, values=hijri_date_adjustment_options, state="readonly", width=25)
                self.hijri_date_adjustment_entry.set(str(hijri_date_adjustment))
                self.hijri_date_adjustment_entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
            
            # Calculation Method
            elif row == 4:
                self.calculation_method_entry = ttk.Combobox(settings_frame, values=calculation_method_options, state="readonly", width=25)
                self.calculation_method_entry.set(calculation_method)
                self.calculation_method_entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
            
            # Asr Method
            elif row == 5:
                self.asr_method_entry = ttk.Combobox(settings_frame, values=asr_method_options, state="readonly", width=25)
                self.asr_method_entry.set(asr_method)
                self.asr_method_entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
        
        # Middle frame
        self.middle_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.middle_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 5))
        
        # Button row in middle frame
        self.middle_button_frame = ttk.Frame(self.middle_frame)
        self.middle_button_frame.pack(side="bottom", pady=10)
        ttk.Button(self.middle_button_frame, text="Restore Defaults", command=self.restore_prayer_defaults).pack(side="left")
        
        header = ["Prayer", "Adhan Time", "", "", "Iqamah Offset (min)"]
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
            ttk.Label(table_frame, text=label, anchor="w", justify="left", font=("TkDefaultFont", 12, "bold")).grid(
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
            
            # Iqamah Offset
            iqamah_offset_entry = ttk.Combobox(table_frame, values=offset_options, state="readonly", width=5)
            iqamah_offset_entry.set(iqamah_offset)
            iqamah_offset_entry.grid(row=row, column=4, padx=4, pady=2, sticky="nsew")
            self.iqamah_offset_entries.append(iqamah_offset_entry)
        
        # Right frame
        self.right_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.right_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        
        # Button row in right frame
        self.right_button_frame = ttk.Frame(self.right_frame)
        self.right_button_frame.pack(side="bottom", pady=10)
        ttk.Button(self.right_button_frame, text="Restore Defaults", command=self.restore_display_defaults).pack(side="left")
        
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
        
        # Masjid Name
        ttk.Label(display_frame, text="Masjid Name", anchor="center", justify="center", font=("TkDefaultFont", 12, "bold")).grid(
            row=0, column=0, padx=4, pady=2, sticky="ew"
        )
        self.name_entry = ttk.Entry(display_frame, width=30, justify="center")
        self.name_entry.insert(0, name)
        self.name_entry.grid(row=1, column=0, padx=4, pady=2, sticky="ew")
        
        # Masjid Address
        ttk.Label(display_frame, text="Masjid Address", anchor="center", justify="center", font=("TkDefaultFont", 12, "bold")).grid(
            row=2, column=0, padx=4, pady=2, sticky="ew"
        )
        self.address_entry = ttk.Entry(display_frame, width=30, justify="center")
        self.address_entry.insert(0, address)
        self.address_entry.grid(row=3, column=0, padx=4, pady=2, sticky="ew")
        
        # Announcements
        ttk.Label(display_frame, text="Announcements", anchor="center", justify="center", font=("TkDefaultFont", 12, "bold")).grid(
            row=4, column=0, padx=4, pady=2, sticky="ew"
        )
        self.announcement_entries = []
        for i in range(5):
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
        
        # Launch button at the bottom
        ttk.Button(self, text="Launch", style="Launch.TButton", command=self.launch).pack(pady=(0, 10))
    
    def launch(self):
        """Launch the main application."""
        
        if not os.path.exists(CSV):
            messagebox.showerror("Error", "CSV file does not exist. Generate CSV file before launching.")
            return
        
        if self.save_settings():
            self.destroy()
            subprocess.Popen(["python", "src/main.py"])
    
    def save_settings(self):
        """Save settings to JSON file."""
        
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
            messagebox.showerror("Error", "Latitude and Longitude must be valid numbers.\n\n(e.g., 40.7128, -74.0060)")
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
            if len(announcement) > 45:
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
            
            # Ensure all parts of time are selected before saving
            if (hour and not minute) or (minute and not hour) or ((hour or minute) and not ampm) or (ampm and not (hour and minute)):
                messagebox.showerror("Error", f"Select hour, minute, and AM/PM for {label}.")
                return False
            adhan_time = f"{hour}:{minute} {ampm}" if hour and minute and ampm else ""
            
            self.settings['DATA']['PRAYERS'][label.upper()] = {
                "ADHAN_TIME": adhan_time,
                "IQAMAH_OFFSET": iqamah_offset,
            }
        
        with open(SETTINGS, "w") as f:
            json.dump(self.settings, f, indent=4)
        
        return True
    
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
        
        self.save_settings()
        fetch_data()
        self.status_var.set("CSV file generated.")
        self.after(1500, self.update_status)
    
    def delete_csv(self):
        """Delete the CSV file."""
        
        if os.path.exists(CSV):
            os.remove(CSV)
            self.status_var.set("CSV file deleted.")
        else:
            self.status_var.set("CSV file does not exist.")

def load_settings():
    """Load settings from JSON file."""
    
    with open(SETTINGS, "r") as f:
        return json.load(f)

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