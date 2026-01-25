import tkinter as tk
from tkinter import ttk
from zoneinfo import available_timezones

class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1100x350")
        self.resizable(False, False)
        # style = ttk.Style()
        # style.theme_use("clam")
        
        # Main container for frames
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
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
        
        settings_labels = ["Latitude", "Longitude", "Timezone", "Hijri Date Adjustment", "Calculation Method", "Asr Method"]
        
        timezones = sorted(available_timezones())
        hijri_adjustments = [f"{i}" for i in range(-1, 2)]
        calc_methods = ["MWL", "ISNA", "Egypt", "Makkah", "Karachi", "Tehran", "Jafari", "France", "Russia", "Singapore"]
        asr_methods = ["Standard", "Hanafi"]
        
        # Settings frame
        settings_frame = ttk.Frame(self.left_frame)
        settings_frame.pack(side="top", fill="x", padx=10, pady=(10, 0))
        
        for row, label in enumerate(settings_labels):
            
            # Labels
            ttk.Label(settings_frame, text=label, anchor="w", font=("TkDefaultFont", 12, "bold")).grid(
                row=row, column=0, padx=4, pady=2, sticky="nsew"
            )
            
            # Latitude and Longitude
            if row == 0 or row == 1:
                ttk.Entry(settings_frame, width=20).grid(
                    row=row, column=1, padx=(30, 0), pady=2, sticky="nsew"
                )
            
            # Timezone
            elif row == 2:
                ttk.Combobox(settings_frame, values=timezones, state="readonly", width=20).grid(
                    row=row, column=1, padx=(30, 0), pady=2, sticky="nsew"
                )
            
            # Hijri Date Adjustment
            elif row == 3:
                ttk.Combobox(settings_frame, values=hijri_adjustments, state="readonly", width=20).grid(
                    row=row, column=1, padx=(30, 0), pady=2, sticky="nsew"
                )
            
            # Calculation Method
            elif row == 4:
                ttk.Combobox(settings_frame, values=calc_methods, state="readonly", width=20).grid(
                    row=row, column=1, padx=(30, 0), pady=2, sticky="nsew"
                )
                
            # Asr Method
            elif row == 5:
                ttk.Combobox(settings_frame, values=asr_methods, state="readonly", width=20).grid(
                    row=row, column=1, padx=(30, 0), pady=2, sticky="nsew"
                )
        
        # Right frame
        self.right_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Button row in right frame
        self.right_button_frame = ttk.Frame(self.right_frame)
        self.right_button_frame.pack(side="bottom", pady=10)
        ttk.Button(self.right_button_frame, text="Restore Defaults").pack(side="left")
        
        header = ["Prayer", "Adhan Time", "", "", "Adjustment (min)", "Iqamah Offset (min)", "Duration (min)"]
        prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Jummah"]
        
        hours = [""] + [f"{h:02d}" for h in range(1, 13)]
        minutes = [""] + [f"{m:02d}" for m in range(0, 60)]
        ampm = [""] + ["AM", "PM"]
        
        adjustment = [f"{i}" for i in range(-5, 6)]
        offset = [f"{i}" for i in range(0, 31, 5)]
        duration = [f"{i}" for i in range(15, 31, 15)]
        
        # Table frame
        table_frame = ttk.Frame(self.right_frame)
        table_frame.pack(side="top", fill="x", padx=10, pady=(10, 0))
        
        # Header row
        for row, label in enumerate(header):
            ttk.Label(table_frame, text=label, anchor="w", justify="left", font=("TkDefaultFont", 12, "bold")).grid(
                row=0, column=row, padx=4, pady=2, sticky="nsew"
            )
        
        # Prayer rows
        for row, label in enumerate(prayers, start=1):
            
            # Prayer Names
            ttk.Label(table_frame, text=label, anchor="w", font=("TkDefaultFont", 12, "bold")).grid(
                row=row, column=0, padx=4, pady=2, sticky="nsew"
            )
            
            # Adhan Time
            ttk.Combobox(table_frame, values=hours, state="readonly", width=5).grid(
                row=row, column=1, padx=4, pady=2, sticky="nsew")
            ttk.Combobox(table_frame, values=minutes, state="readonly", width=5).grid(
                row=row, column=2, padx=4, pady=2, sticky="nsew")
            ttk.Combobox(table_frame, values=ampm, state="readonly", width=5).grid(
                row=row, column=3, padx=4, pady=2, sticky="nsew")
            
            # Adjustment
            ttk.Combobox(table_frame, values=adjustment, state="readonly", width=5).grid(
                row=row, column=4, padx=4, pady=2, sticky="nsew")
            
            # Iqamah Offset
            ttk.Combobox(table_frame, values=offset, state="readonly", width=5).grid(
                row=row, column=5, padx=4, pady=2, sticky="nsew")
            
            # Duration
            ttk.Combobox(table_frame, values=duration, state="readonly", width=5).grid(
                row=row, column=6, padx=4, pady=2, sticky="nsew")
        
        # Configure grid weights for main frame
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(0, weight=1)
        
        # Launch button at the bottom
        ttk.Button(self, text="Launch").pack(pady=(0, 10))

if __name__ == "__main__":
    app = Launcher()
    app.mainloop()