import tkinter as tk
from tkinter import ttk

class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x400")
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
        ttk.Button(self.left_button_frame, text="Delete CSV").pack(side="left", padx=(5,0))
        
        # Status label
        self.status_var = tk.StringVar(value="Status")
        self.status_entry = ttk.Entry(self.left_frame, textvariable=self.status_var, state="readonly", justify="center")
        self.status_entry.pack(side="bottom", fill="x", padx=10)
        
        # Right frame
        self.right_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Button row in right frame
        self.right_button_frame = ttk.Frame(self.right_frame)
        self.right_button_frame.pack(side="bottom", pady=10)
        ttk.Button(self.right_button_frame, text="Save Changes").pack(side="left")
        ttk.Button(self.right_button_frame, text="Restore Defaults").pack(side="left", padx=10)
        
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
        for col, text in enumerate(header):
            lbl = ttk.Label(table_frame, text=text, anchor="w", justify="left", font=("TkDefaultFont", 12, "bold"))
            lbl.grid(row=0, column=col, padx=4, pady=2, sticky="nsew")
        
        # Prayer rows
        for row, prayer in enumerate(prayers, start=1):
            # Prayer name
            lbl = ttk.Label(table_frame, text=prayer, anchor="w")
            lbl.grid(row=row, column=0, padx=4, pady=2, sticky="nsew")
            
            # Adhan Time: hours, minutes, am/pm
            cb_hour = ttk.Combobox(table_frame, values=hours, state="readonly", width=5)
            cb_hour.grid(row=row, column=1, padx=4, pady=2, sticky="nsew")
            cb_min = ttk.Combobox(table_frame, values=minutes, state="readonly", width=5)
            cb_min.grid(row=row, column=2, padx=4, pady=2, sticky="nsew")
            cb_ampm = ttk.Combobox(table_frame, values=ampm, state="readonly", width=5)
            cb_ampm.grid(row=row, column=3, padx=4, pady=2, sticky="nsew")
            
            # Adjustment (min)
            cb_adj = ttk.Combobox(table_frame, values=adjustment, state="readonly", width=5)
            cb_adj.grid(row=row, column=4, padx=4, pady=2, sticky="nsew")
            
            # Iqamah Offset (min)
            cb_offset = ttk.Combobox(table_frame, values=offset, state="readonly", width=5)
            cb_offset.grid(row=row, column=5, padx=4, pady=2, sticky="nsew")
            
            # Duration (min)
            cb_dur = ttk.Combobox(table_frame, values=duration, state="readonly", width=5)
            cb_dur.grid(row=row, column=6, padx=4, pady=2, sticky="nsew")
        
        # Configure grid weights for main frame
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(0, weight=1)
        
        # Launch button at the bottom
        self.bottom_button = ttk.Button(self, text="Launch")
        self.bottom_button.pack(pady=(0, 10))

if __name__ == "__main__":
    app = Launcher()
    app.mainloop()