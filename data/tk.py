import tkinter as tk
from tkinter import ttk, messagebox
import json
from zoneinfo import available_timezones
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data import refresh_data, fetch_data, save_data
import datetime
import shutil

SETTINGS = "data/settings.json"
CSV = "data/data.csv"

CALC_METHODS = [
    "MWL", "ISNA", "Egypt", "Makkah", "Karachi", "Tehran", "Jafari", "France", "Russia", "Singapore"
]

ASR_METHODS = ["Standard", "Hanafi"]

def load_settings():
    with open(SETTINGS, "r") as f:
        return json.load(f)

def save_settings(settings):
    # Read current settings
    with open(SETTINGS, "r") as f:
        current = json.load(f)
    # Only backup if there are changes
    if current != settings:
        backup_settings()
    with open(SETTINGS, "w") as f:
        json.dump(settings, f, indent=4)

def backup_settings():
    backup_name = f"data/backups/settings_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    shutil.copy2(SETTINGS, backup_name)

def tooltip(widget, text):
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

class SettingsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.resizable(False, False)
        self.settings = load_settings()
        self.original_settings = json.loads(json.dumps(self.settings))  # Deep copy
        self.create_widgets()
        style = ttk.Style()
        style.theme_use("clam")

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Display Tab
        self.display_frame = ttk.Frame(notebook)
        # notebook.add(self.display_frame, text="Display")
        self.create_display_tab(self.display_frame)

        # Data Tab
        self.data_frame = ttk.Frame(notebook)
        notebook.add(self.data_frame, text="Data")
        self.create_data_tab(self.data_frame)

        # Refresh Data Status
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self, textvariable=self.status_var)
        self.status_label.pack(pady=5)
        self.update_status()
        
        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        save_btn = ttk.Button(btn_frame, text="Save Changes", command=self.save_changes)
        save_btn.pack(side="left", padx=(0,10))
        restore_btn = ttk.Button(btn_frame, text="Restore Defaults", command=self.restore_defaults)
        restore_btn.pack(side="left", padx=(10,10))
        refresh_btn = ttk.Button(btn_frame, text="Refresh Data", command=self.refresh_data)
        refresh_btn.pack(side="left", padx=(10,10))
        delete_btn = ttk.Button(btn_frame, text="Delete CSV", command=self.delete_csv)
        delete_btn.pack(side="left", padx=(10,0))

    def create_display_tab(self, frame):
        display = self.settings["DISPLAY"]

        ttk.Label(frame, text="Masjid Name:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.name_var = tk.StringVar(value=display["NAME"])
        ttk.Entry(frame, textvariable=self.name_var, width=40).grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Address:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.address_var = tk.StringVar(value=display["ADDRESS"])
        ttk.Entry(frame, textvariable=self.address_var, width=40).grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Announcements:").grid(row=2, column=0, sticky="nw", pady=5, padx=5)
        self.announcements_text = tk.Text(frame, width=40, height=8)
        self.announcements_text.grid(row=2, column=1, pady=5, padx=5)
        self.announcements_text.insert("1.0", "\n".join(display.get("ANNOUNCEMENTS", [])))

    def create_data_tab(self, frame):
        data = self.settings["DATA"]
        
        loc = data["LOCATION"]
        ttk.Label(frame, text="Latitude, Longitude:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.lat_var = tk.DoubleVar(value=loc["LATITUDE"])
        self.lon_var = tk.DoubleVar(value=loc["LONGITUDE"])
        
        latlon_frame = ttk.Frame(frame)
        latlon_frame.grid(row=0, column=1, pady=5, padx=125, sticky="w")
        
        lat_entry = ttk.Entry(latlon_frame, textvariable=self.lat_var, width=14)
        lat_entry.pack(side="left", padx=10)
        
        lon_entry = ttk.Entry(latlon_frame, textvariable=self.lon_var, width=14)
        lon_entry.pack(side="right", padx=10)

        coord_help = (
            "To find your Latitude and Longitude:\n\n"
            "1. Open Google Maps (https://maps.google.com)\n"
            "2. Right-click your location.\n"
            "3. The coordinates (latitude, longitude) appear at the top of the menu — click to copy.\t\n"
            "4. Enter each value in its respective box.\n"
        )

        tooltip(lat_entry, coord_help)
        tooltip(lon_entry, coord_help)

        ttk.Label(frame, text="Timezone:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        timezones = sorted([tz for tz in available_timezones() if "/" in tz and not tz.startswith("Etc/")])
        self.tz_var = tk.StringVar(value=loc["TIMEZONE"])
        self.tz_combo = ttk.Combobox(frame, textvariable=self.tz_var, values=timezones, width=29, state="readonly").grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Hijri Date Adjustment:").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        self.hijri_adj_var = tk.StringVar(value=str(loc.get("HIJRI_DATE_ADJUSTMENT")))
        self.hijri_adj_combo = ttk.Combobox(frame, textvariable=self.hijri_adj_var, values=[str(x) for x in list(range(-1, 2))], width=29, state="readonly").grid(row=3, column=1, pady=5, padx=5)
        
        calc = data["CALCULATION"]
        ttk.Label(frame, text="Calculation Method:").grid(row=4, column=0, sticky="w", pady=5, padx=5)
        self.method_var = tk.StringVar(value=calc["METHOD"])
        self.method_combo = ttk.Combobox(frame, textvariable=self.method_var, values=CALC_METHODS, width=29, state="readonly").grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Asr Method:").grid(row=5, column=0, sticky="w", pady=5, padx=5)
        self.asr_var = tk.StringVar(value=calc["ASR_METHOD"])
        self.asr_combo = ttk.Combobox(frame, textvariable=self.asr_var, values=ASR_METHODS, width=29, state="readonly").grid(row=5, column=1, pady=5, padx=5)

        csv = data["CSV"]
        ttk.Label(frame, text="Fetch Window (days):").grid(row=6, column=0, sticky="w", pady=5, padx=5)
        self.fetch_var = tk.IntVar(value=csv["FETCH_WINDOW"])
        ttk.Entry(frame, textvariable=self.fetch_var, width=30).grid(row=6, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Refresh Interval (days):").grid(row=7, column=0, sticky="w", pady=5, padx=5)
        self.refresh_var = tk.IntVar(value=csv["REFRESH_INTERVAL"])
        ttk.Entry(frame, textvariable=self.refresh_var, width=30).grid(row=7, column=1, pady=5, padx=5)
        
        # Create a separate frame for the prayer table to isolate its column configuration
        table_frame = ttk.Frame(frame)
        table_frame.grid(row=9, column=0, columnspan=5, sticky="w", padx=5, pady=10)
        
        prayers = "Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Jummah"
        
        # Table headers
        headers = ["Prayer", "Adhan Time", "Adjustment (min)", "Iqamah Offset (min)", "Duration (min)"]
        for col, header in enumerate(headers):
            ttk.Label(table_frame, text=header).grid(row=0, column=col, padx=5, pady=5, sticky="w")

        self.prayer_entries = {}

        # Generate dropdown options
        hour_options = [f"{h:02d}" for h in range(1, 13)]
        minute_options = [f"{m:02d}" for m in range(0, 60, 5)]
        am_pm_options = ["AM", "PM"]
        adj_options = [str(i) for i in range(-10, 11)]
        iqamah_options = [str(m) for m in range(0, 35, 5)]
        duration_options = [str(m) for m in range(10, 35, 5)]

        for i, prayer in enumerate(prayers):
            prayer_key = prayer.upper()
            row = 1 + i
            ttk.Label(table_frame, text=prayer).grid(row=row, column=0, padx=(0, 5), pady=5, sticky="w")

            # Adhan Time - Parse existing time if present
            adhan_time = data["PRAYERS"].get(prayer_key, {}).get("ADHAN_TIME", "")
            hour_part = ""
            minute_part = ""
            am_pm_part = ""
            
            if adhan_time:
                parts = adhan_time.split()
                if len(parts) == 2:
                    time_parts = parts[0].split(":")
                    if len(time_parts) == 2:
                        hour_part = time_parts[0]
                        minute_part = time_parts[1]
                    am_pm_part = parts[1]
            
            adhan_hour_var = tk.StringVar(value=hour_part)
            adhan_minute_var = tk.StringVar(value=minute_part)
            adhan_am_pm_var = tk.StringVar(value=am_pm_part)
            
            time_frame = ttk.Frame(table_frame)
            time_frame.grid(row=row, column=1, padx=5, pady=5, sticky="w")
            
            # Hour dropdown
            hour_combo = ttk.Combobox(time_frame, textvariable=adhan_hour_var, values=hour_options, width=4, state="readonly")
            hour_combo.pack(side="left", padx=5)
            
            # Minute dropdown
            minute_combo = ttk.Combobox(time_frame, textvariable=adhan_minute_var, values=minute_options, width=4, state="readonly")
            minute_combo.pack(side="left", padx=5)
            
            # AM/PM dropdown
            am_pm_combo = ttk.Combobox(time_frame, textvariable=adhan_am_pm_var, values=am_pm_options, width=4, state="readonly")
            am_pm_combo.pack(side="left", padx=5)
            
            def make_clear_fn(h=adhan_hour_var, m=adhan_minute_var, a=adhan_am_pm_var):
                return lambda: (h.set(""), m.set(""), a.set(""))
            
            clear_btn = ttk.Button(time_frame, text="x", width=1, style="Clear.TButton", padding=(1,0), command=make_clear_fn())
            clear_btn.pack(side="left", padx=5)
            
            # Adjustment
            adj_var = tk.StringVar(value=str(data["PRAYERS"].get(prayer_key, {}).get("ADJUSTMENT")))
            adj_combo = ttk.Combobox(table_frame, textvariable=adj_var, values=adj_options, width=12, state="readonly")
            adj_combo.grid(row=row, column=2, padx=5, pady=5, sticky="w")

            # Iqamah Offset
            iqamah_var = tk.StringVar(value=f"{data['PRAYERS'].get(prayer_key, {}).get('IQAMAH_OFFSET')}")
            iqamah_combo = ttk.Combobox(table_frame, textvariable=iqamah_var, values=iqamah_options, width=12, state="readonly")
            iqamah_combo.grid(row=row, column=3, padx=5, pady=5, sticky="w")

            # Duration
            duration_var = tk.StringVar(value=f"{data['PRAYERS'].get(prayer_key, {}).get('DURATION')}")
            duration_combo = ttk.Combobox(table_frame, textvariable=duration_var, values=duration_options, width=12, state="readonly")
            duration_combo.grid(row=row, column=4, padx=5, pady=5, sticky="w")
            
            self.prayer_entries[prayer_key] = {
                "ADHAN_HOUR": adhan_hour_var,
                "ADHAN_MINUTE": adhan_minute_var,
                "ADHAN_AMPM": adhan_am_pm_var,
                "ADJUSTMENT": adj_var,
                "IQAMAH_OFFSET": iqamah_var,
                "DURATION": duration_var
            }

    def restore_defaults(self):
        # Reload from the original loaded settings
        self.settings = json.loads(json.dumps(self.original_settings))  # Deep copy

        # Update Display tab
        display = self.settings["DISPLAY"]
        self.name_var.set(display["NAME"])
        self.address_var.set(display["ADDRESS"])
        self.announcements_text.delete("1.0", "end")
        self.announcements_text.insert("1.0", "\n".join(display.get("ANNOUNCEMENTS", [])))

        # Update Data tab
        data = self.settings["DATA"]
        loc = data["LOCATION"]
        self.lat_var.set(loc["LATITUDE"])
        self.lon_var.set(loc["LONGITUDE"])
        self.tz_var.set(loc["TIMEZONE"])
        self.hijri_adj_var.set(str(loc.get("HIJRI_DATE_ADJUSTMENT")))

        calc = data["CALCULATION"]
        self.method_var.set(calc["METHOD"])
        self.asr_var.set(calc["ASR_METHOD"])

        csv = data["CSV"]
        self.fetch_var.set(csv["FETCH_WINDOW"])
        self.refresh_var.set(csv["REFRESH_INTERVAL"])
        
        prayers = data["PRAYERS"]
        for prayer_key, entries in self.prayer_entries.items():
            prayer_data = prayers.get(prayer_key, {})
            adhan_time = prayer_data.get("ADHAN_TIME", "")
            hour_part = ""
            minute_part = ""
            am_pm_part = ""
            if adhan_time:
                parts = adhan_time.split()
                if len(parts) == 2:
                    time_parts = parts[0].split(":")
                    if len(time_parts) == 2:
                        hour_part = time_parts[0]
                        minute_part = time_parts[1]
                    am_pm_part = parts[1]
            entries["ADHAN_HOUR"].set(hour_part)
            entries["ADHAN_MINUTE"].set(minute_part)
            entries["ADHAN_AMPM"].set(am_pm_part)
            entries["ADJUSTMENT"].set(prayer_data.get("ADJUSTMENT"))
            entries["IQAMAH_OFFSET"].set(prayer_data.get("IQAMAH_OFFSET"))
            entries["DURATION"].set(prayer_data.get("DURATION"))
        
        save_settings(self.settings)
        messagebox.showinfo("Restored", "Settings restored to original loaded values.")

    def save_changes(self):
        # Validate latitude and longitude
        try:
            lat = float(self.lat_var.get())
            lon = float(self.lon_var.get())
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError("Latitude must be between -90 and 90, and Longitude between -180 and 180.")
        except Exception as e:
            messagebox.showerror("Invalid Input", f"Latitude/Longitude error:\n{e}")
            return

        # Validate fetch window and refresh interval
        try:
            fetch_window = int(self.fetch_var.get())
            refresh_interval = int(self.refresh_var.get())
            if fetch_window <= 0 or refresh_interval <= 0:
                raise ValueError("Fetch Window and Refresh Interval must be positive integers.")
        except Exception as e:
            messagebox.showerror("Invalid Input", f"Fetch/Refresh error:\n{e}")
            return

        self.settings["DISPLAY"]["NAME"] = self.name_var.get()
        self.settings["DISPLAY"]["ADDRESS"] = self.address_var.get()
        announcements = self.announcements_text.get("1.0", "end").strip().splitlines()
        self.settings["DISPLAY"]["ANNOUNCEMENTS"] = [a for a in announcements if a.strip()]

        loc = self.settings["DATA"]["LOCATION"]
        loc["LATITUDE"] = lat
        loc["LONGITUDE"] = lon
        loc["TIMEZONE"] = self.tz_var.get()
        loc["HIJRI_DATE_ADJUSTMENT"] = int(self.hijri_adj_var.get())

        calc = self.settings["DATA"]["CALCULATION"]
        calc["METHOD"] = self.method_var.get()
        calc["ASR_METHOD"] = self.asr_var.get()

        csv = self.settings["DATA"]["CSV"]
        csv["FETCH_WINDOW"] = fetch_window
        csv["REFRESH_INTERVAL"] = refresh_interval
        
        prayers = self.settings["DATA"]["PRAYERS"]
        for prayer_key, entries in self.prayer_entries.items():
            hour = entries["ADHAN_HOUR"].get()
            minute = entries["ADHAN_MINUTE"].get()
            am_pm = entries["ADHAN_AMPM"].get()
            if hour and minute and am_pm:
                adhan_time = f"{hour}:{minute} {am_pm}"
            else:
                adhan_time = ""
            prayers[prayer_key] = {
                "ADHAN_TIME": adhan_time,
                "ADJUSTMENT": int(entries["ADJUSTMENT"].get()),
                "IQAMAH_OFFSET": int(entries["IQAMAH_OFFSET"].get()),
                "DURATION": int(entries["DURATION"].get())
            }

        try:
            save_settings(self.settings)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings:\n{e}")
        self.update_status()
            
    def update_status(self):
        if refresh_data():
            self.status_var.set("Data needs refresh.")
        else:
            self.status_var.set("Data does not need refresh.")

    def refresh_data(self):
        if refresh_data():
            rows = fetch_data()
            if save_data(rows):
                self.status_var.set("Data refreshed successfully!")
            else:
                self.status_var.set("Error refreshing data.")
        else:
            self.status_var.set("Data is up to date. No refresh needed.")

    def delete_csv(self):
        if os.path.exists(CSV):
            try:
                os.remove(CSV)
                self.status_var.set("CSV deleted. Please refresh data.")
                messagebox.showinfo("Deleted", "CSV file deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete CSV:\n{e}")
        else:
            messagebox.showinfo("Info", "CSV file does not exist.")

if __name__ == "__main__":
    app = SettingsApp()
    app.mainloop()