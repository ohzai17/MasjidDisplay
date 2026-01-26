import json
import tkinter as tk
from tkinter import ttk
from zoneinfo import available_timezones

SETTINGS = 'data/settings.json'

def load_settings():
    with open(SETTINGS, "r") as f:
        return json.load(f)

def ToolTip(widget, text):
    
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
        label = tk.Label(tw, text=text, justify='left', background="#ffffe0", relief='solid', borderwidth=1)
        label.pack(ipadx=1)
    
    def hide_tip(event=None):
        nonlocal tipwindow
        if tipwindow:
            tipwindow.destroy()
            tipwindow = None
    
    widget.bind("<Enter>", show_tip)
    widget.bind("<Leave>", hide_tip)

class Launcher(tk.Tk):
    def __init__(self):
        
        super().__init__()
        self.geometry("1500x400")
        self.resizable(False, False)
        # style = ttk.Style()
        # style.theme_use("clam")
        
        # Main container for frames
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load settings
        settings = load_settings()
        display = settings["DISPLAY"]
        location = settings['DATA']['LOCATION']
        calculation = settings['DATA']['CALCULATION']
        prayers = settings['DATA']['PRAYERS']
        
        # Left frame
        self.left_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Button row in left frame
        self.left_button_frame = ttk.Frame(self.left_frame)
        self.left_button_frame.pack(side="bottom", pady=10)
        ttk.Button(self.left_button_frame, text="Generate CSV").pack(side="left")
        ttk.Button(self.left_button_frame, text="Delete CSV").pack(side="left", padx=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Status")
        self.status_entry = ttk.Entry(self.left_frame, textvariable=self.status_var, state="readonly", justify="center")
        self.status_entry.pack(side="bottom", fill="x", padx=10)
        
        setting_labels = ["Latitude", "Longitude", "Timezone", "Hijri Date Adjustment", "Calculation Method", "Asr Method"]
        
        timezone_options = sorted(available_timezones())
        hijri_date_adjustment_options = [f"{i}" for i in range(-1, 2)]
        calculation_method_options = ["MWL", "ISNA", "Egypt", "Makkah", "Karachi", "Tehran", "Jafari", "France", "Russia", "Singapore"]
        asr_method_options = ["Standard", "Hanafi"]
        
        latitude = location.get("LATITUDE", "")
        longitude = location.get("LONGITUDE", "")
        timezone = location.get("TIMEZONE", "America/New_York")
        hijri_date_adjustment = location.get("HIJRI_DATE_ADJUSTMENT", 0)
        calculation_method = calculation.get("METHOD", "ISNA")
        asr_method = calculation.get("ASR_METHOD", "Standard")
        
        # Settings frame
        settings_frame = ttk.Frame(self.left_frame)
        settings_frame.pack(side="top", fill="x", padx=10, pady=(10, 0))
        
        for row, label in enumerate(setting_labels):
            
            # Labels
            ttk.Label(settings_frame, text=label, anchor="w", font=("TkDefaultFont", 12, "bold")).grid(
                row=row, column=0, padx=4, pady=2, sticky="nsew"
            )
            
            coord_help = (
                "To find your Latitude and Longitude:\n\n"
                "1. Open Google Maps (https://maps.google.com)\n"
                "2. Right-click your location.\n"
                "3. The coordinates (latitude, longitude) appear at the top of the menu — click to copy.\t\n"
                "4. Enter each value in its respective box.\n"
            )
            
            # Latitude
            if row == 0:
                entry = ttk.Entry(settings_frame, width=20)
                entry.insert(0, latitude)
                entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
                ToolTip(entry, coord_help)
            
            # Longitude
            elif row == 1:
                entry = ttk.Entry(settings_frame, width=20)
                entry.insert(0, longitude)
                entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
                ToolTip(entry, coord_help)
            
            # Timezone
            elif row == 2:
                entry = ttk.Combobox(settings_frame, values=timezone_options, state="readonly", width=20)
                entry.set(timezone)
                entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
            
            # Hijri Date Adjustment
            elif row == 3:
                entry = ttk.Spinbox(settings_frame, values=hijri_date_adjustment_options, state="readonly", width=20)
                entry.set(str(hijri_date_adjustment))
                entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
            
            # Calculation Method
            elif row == 4:
                entry = ttk.Combobox(settings_frame, values=calculation_method_options, state="readonly", width=20)
                entry.set(calculation_method)
                entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
            
            # Asr Method
            elif row == 5:
                entry = ttk.Combobox(settings_frame, values=asr_method_options, state="readonly", width=20)
                entry.set(asr_method)
                entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
        
        # Middle frame
        self.middle_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.middle_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 5))
        
        # Button row in middle frame
        self.middle_button_frame = ttk.Frame(self.middle_frame)
        self.middle_button_frame.pack(side="bottom", pady=10)
        ttk.Button(self.middle_button_frame, text="Restore Defaults").pack(side="left")
        
        header = ["Prayer", "Adhan Time", "", "", "Adjustment (min)", "Iqamah Offset (min)", "Duration (min)"]
        prayer_labels = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Jummah"]
        
        hours_options = [""] + [f"{i:02d}" for i in range(1, 13)]
        minutes_options = [""] + [f"{i:02d}" for i in range(0, 60, 5)]
        ampm_options = [""] + ["AM", "PM"]
        
        adjustment_options = [f"{i}" for i in range(-10, 11)]
        offset_options = [f"{i}" for i in range(0, 31, 5)]
        duration_options = [f"{i}" for i in range(15, 31, 15)]
        
        # Table frame
        table_frame = ttk.Frame(self.middle_frame)
        table_frame.pack(side="top", fill="x", padx=10, pady=(10, 0))
        
        # Header row
        for row, label in enumerate(header):
            ttk.Label(table_frame, text=label, anchor="w", justify="left", font=("TkDefaultFont", 12, "bold")).grid(
                row=0, column=row, padx=4, pady=2, sticky="nsew"
            )
        
        # Prayer rows
        for row, label in enumerate(prayer_labels, start=1):
            
            prayer = prayers.get(label.upper(), {})
            adhan_time = prayer.get("ADHAN_TIME", "")
            adjustment = prayer.get("ADJUSTMENT", 0)
            iqamah_offset = prayer.get("IQAMAH_OFFSET", 0)
            duration = prayer.get("DURATION", 15)
            
            hours, minutes, ampm = "", "", ""
            if adhan_time:
                hhmm, ampm = adhan_time.split()
                hours, minutes = hhmm.split(":")
            
            # Prayer Names
            ttk.Label(table_frame, text=label, anchor="w", font=("TkDefaultFont", 12, "bold")).grid(
                row=row, column=0, padx=4, pady=2, sticky="nsew"
            )
            
            # Adhan Time
            entry = ttk.Combobox(table_frame, values=hours_options, state="readonly", width=5)
            entry.set(hours)
            entry.grid(row=row, column=1, padx=4, pady=2, sticky="nsew")
            entry = ttk.Combobox(table_frame, values=minutes_options, state="readonly", width=5)
            entry.set(minutes)
            entry.grid(row=row, column=2, padx=4, pady=2, sticky="nsew")
            entry = ttk.Combobox(table_frame, values=ampm_options, state="readonly", width=5)
            entry.set(ampm)
            entry.grid(row=row, column=3, padx=4, pady=2, sticky="nsew")
            
            # Adjustment
            entry = ttk.Spinbox(table_frame, values=adjustment_options, state="readonly", width=5)
            entry.set(adjustment)
            entry.grid(row=row, column=4, padx=4, pady=2, sticky="nsew")
            
            # Iqamah Offset
            entry = ttk.Combobox(table_frame, values=offset_options, state="readonly", width=5)
            entry.set(iqamah_offset)
            entry.grid(row=row, column=5, padx=4, pady=2, sticky="nsew")
            
            # Duration
            entry = ttk.Combobox(table_frame, values=duration_options, state="readonly", width=5)
            entry.set(duration)
            entry.grid(row=row, column=6, padx=4, pady=2, sticky="nsew")
        
        # Right frame
        self.right_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.right_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        
        # Button row in right frame
        self.right_button_frame = ttk.Frame(self.right_frame)
        self.right_button_frame.pack(side="bottom", pady=10)
        ttk.Button(self.right_button_frame, text="Restore Defaults").pack(side="left")
        
        announcement_options = [
            "",
            "Eid Al-Fitr Salah: Month DD, YYYY @ HH:MM AM",
            "Zakat Al-Fitr: $XX Per Person",
            "Eid Al-Adha Salah: Month DD, YYYY @ HH:MM AM"
        ]
        
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
        entry = ttk.Entry(display_frame, width=30, justify="center")
        entry.insert(0, name)
        entry.grid(row=1, column=0, padx=4, pady=2, sticky="ew")

        # Masjid Address
        ttk.Label(display_frame, text="Masjid Address", anchor="center", justify="center", font=("TkDefaultFont", 12, "bold")).grid(
            row=2, column=0, padx=4, pady=2, sticky="ew"
        )
        entry = ttk.Entry(display_frame, width=30, justify="center")
        entry.insert(0, address)
        entry.grid(row=3, column=0, padx=4, pady=2, sticky="ew")

        # Announcements
        ttk.Label(display_frame, text="Announcements", anchor="center", justify="center", font=("TkDefaultFont", 12, "bold")).grid(
            row=4, column=0, padx=4, pady=2, sticky="ew"
        )
        for i in range(5):
            entry = ttk.Combobox(display_frame, values=announcement_options, width=30, justify="center")
            if i < len(announcements):
                entry.set(announcements[i])
            entry.grid(row=5 + i, column=0, padx=4, pady=2, sticky="ew")
        
        # Configure grid weights for main frame
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=8)
        self.main_frame.rowconfigure(0, weight=1)
        
        # Launch button at the bottom
        ttk.Button(self, text="Launch").pack(pady=(0, 10))

if __name__ == "__main__":
    app = Launcher()
    app.mainloop()