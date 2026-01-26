import tkinter as tk
from tkinter import ttk
from zoneinfo import available_timezones

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
            
            coord_help = (
                "To find your Latitude and Longitude:\n\n"
                "1. Open Google Maps (https://maps.google.com)\n"
                "2. Right-click your location.\n"
                "3. The coordinates (latitude, longitude) appear at the top of the menu — click to copy.\t\n"
                "4. Enter each value in its respective box.\n"
            )
            
            # Latitude and Longitude
            if row == 0 or row == 1:
                entry = ttk.Entry(settings_frame, width=20)
                entry.grid(row=row, column=1, padx=(30, 0), pady=2, sticky="nsew")
                ToolTip(entry, coord_help)
            
            # Timezone
            elif row == 2:
                ttk.Combobox(settings_frame, values=timezones, state="readonly", width=20).grid(
                    row=row, column=1, padx=(30, 0), pady=2, sticky="nsew"
                )
            
            # Hijri Date Adjustment
            elif row == 3:
                ttk.Spinbox(settings_frame, values=hijri_adjustments, state="readonly", width=20).grid(
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
        
        # Middle frame
        self.middle_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.middle_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 5))
        
        # Button row in middle frame
        self.middle_button_frame = ttk.Frame(self.middle_frame)
        self.middle_button_frame.pack(side="bottom", pady=10)
        ttk.Button(self.middle_button_frame, text="Restore Defaults").pack(side="left")
        
        header = ["Prayer", "Adhan Time", "", "", "Adjustment (min)", "Iqamah Offset (min)", "Duration (min)"]
        prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Jummah"]
        
        hours = [""] + [f"{h:02d}" for h in range(1, 13)]
        minutes = [""] + [f"{m:02d}" for m in range(0, 60)]
        ampm = [""] + ["AM", "PM"]
        
        adjustment = [f"{i}" for i in range(-10, 11)]
        offset = [f"{i}" for i in range(0, 31, 5)]
        duration = [f"{i}" for i in range(15, 31, 15)]
        
        # Table frame
        table_frame = ttk.Frame(self.middle_frame)
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
                row=row, column=1, padx=4, pady=2, sticky="nsew"
            )
            ttk.Combobox(table_frame, values=minutes, state="readonly", width=5).grid(
                row=row, column=2, padx=4, pady=2, sticky="nsew"
            )
            ttk.Combobox(table_frame, values=ampm, state="readonly", width=5).grid(
                row=row, column=3, padx=4, pady=2, sticky="nsew"
            )
            
            # Adjustment
            ttk.Spinbox(table_frame, values=adjustment, state="readonly", width=5).grid(
                row=row, column=4, padx=4, pady=2, sticky="nsew"
            )
            
            # Iqamah Offset
            ttk.Combobox(table_frame, values=offset, state="readonly", width=5).grid(
                row=row, column=5, padx=4, pady=2, sticky="nsew"
            )
            
            # Duration
            ttk.Combobox(table_frame, values=duration, state="readonly", width=5).grid(
                row=row, column=6, padx=4, pady=2, sticky="nsew"
            )
        
        # Right frame
        self.right_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.right_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        
        # Button row in right frame
        self.right_button_frame = ttk.Frame(self.right_frame)
        self.right_button_frame.pack(side="bottom", pady=10)
        ttk.Button(self.right_button_frame, text="Restore Defaults").pack(side="left")
        
        announcement_templates = [
            "",
            "Eid Al-Fitr Salah: Month DD, YYYY @ HH:MM AM",
            "Zakat Al-Fitr: $XX Per Person",
            "Eid Al-Adha Salah: Month DD, YYYY @ HH:MM AM"
        ]
        
        # Display frame
        display_frame = ttk.Frame(self.right_frame)
        display_frame.pack(side="top", fill="x", padx=10, pady=(10, 0))
        display_frame.columnconfigure(0, weight=1)
        
        # Masjid Name
        ttk.Label(display_frame, text="Masjid Name", anchor="center", justify="center", font=("TkDefaultFont", 12, "bold")).grid(
            row=0, column=0, padx=4, pady=2, sticky="ew"
        )
        ttk.Entry(display_frame, width=30, justify="center").grid(
            row=1, column=0, padx=4, pady=2, sticky="ew"
        )

        # Masjid Address
        ttk.Label(display_frame, text="Masjid Address", anchor="center", justify="center", font=("TkDefaultFont", 12, "bold")).grid(
            row=2, column=0, padx=4, pady=2, sticky="ew"
        )
        ttk.Entry(display_frame, width=30, justify="center").grid(
            row=3, column=0, padx=4, pady=2, sticky="ew"
        )

        # Announcements
        ttk.Label(display_frame, text="Announcements", anchor="center", justify="center", font=("TkDefaultFont", 12, "bold")).grid(
            row=4, column=0, padx=4, pady=2, sticky="ew"
        )
        for i in range(5):
            ttk.Combobox(display_frame, values=announcement_templates, width=30, justify="center").grid(
                row=5 + i, column=0, padx=4, pady=2, sticky="ew"
            )
        
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