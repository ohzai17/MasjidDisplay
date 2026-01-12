import tkinter as tk
from tkinter import ttk, messagebox
import json
from zoneinfo import available_timezones
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data import refresh_data, fetch_data, save_data

SETTINGS_PATH = "data/settings.json"

CALC_METHODS = [
    "MWL", "ISNA", "Egypt", "Makkah", "Karachi", "Tehran", "Jafari", "France", "Russia", "Singapore"
]

ASR_METHODS = ["Standard", "Hanafi"]

HIJRI_ADJUSTMENTS = [-1, 0, 1]

def load_settings():
    with open(SETTINGS_PATH, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

class SettingsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
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
        restore_btn.pack(side="left", padx=(10,0))
        
        ref_btn_frame = ttk.Frame(self)
        ref_btn_frame.pack(pady=10)
        refresh_btn = ttk.Button(ref_btn_frame, text="Refresh Data", command=self.refresh_data)
        refresh_btn.pack(side="left")

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
        ttk.Label(frame, text="Latitude:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.lat_var = tk.DoubleVar(value=loc["LATITUDE"])
        ttk.Entry(frame, textvariable=self.lat_var, width=30).grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Longitude:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.lon_var = tk.DoubleVar(value=loc["LONGITUDE"])
        ttk.Entry(frame, textvariable=self.lon_var, width=30).grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Timezone:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        timezones = sorted([tz for tz in available_timezones() if "/" in tz and not tz.startswith("Etc/")])
        self.tz_var = tk.StringVar(value=loc["TIMEZONE"])
        self.tz_combo = ttk.Combobox(frame, textvariable=self.tz_var, values=timezones, width=29, state="readonly").grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Hijri Date Adjustment:").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        self.hijri_adj_var = tk.StringVar(value=str(loc.get("HIJRI_DATE_ADJUSTMENT")))
        self.hijri_adj_combo = ttk.Combobox(frame, textvariable=self.hijri_adj_var, values=[str(x) for x in HIJRI_ADJUSTMENTS], width=29, state="readonly").grid(row=3, column=1, pady=5, padx=5)
        
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

if __name__ == "__main__":
    app = SettingsApp()
    app.mainloop()