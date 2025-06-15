import tkinter as tk
from tkinter import ttk, messagebox
import math

class ControlPanel(tk.Tk):
    def __init__(self, add_body_callback, search_callback):
        super().__init__()
        self.title("Space model - Control")
        self.geometry("350x500")

        ttk.Label(self, text="Gravitational constant G").pack(pady=5)
        self.entry_G = ttk.Entry(self)
        self.entry_G.pack(fill='x', padx=20)
        self.entry_G.insert(0, "1000")
        self.btn_set_G = ttk.Button(self, text="Set G", command=self.set_G)
        self.btn_set_G.pack(pady=5)
        self.G = 1000.0

        ttk.Label(self, text="Create new body").pack(pady=10)
        frame = ttk.Frame(self)
        frame.pack(padx=10, fill='x')

        labels = ["Name:", "X:", "Y:", "Speed:", "Angle(deg.):", "Weight:", "Radius:"]
        defaults = ["Body1", "400", "300", "0", "0", "100", "15"]
        self.entries = {}

        for i, (label, default) in enumerate(zip(labels, defaults)):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky='w')
            entry = ttk.Entry(frame, width=15)
            entry.grid(row=i, column=1, sticky='w')
            entry.insert(0, default)
            self.entries[label] = entry

        self.add_body_callback = add_body_callback
        self.btn_add = ttk.Button(self, text="Add body", command=self.add_body)
        self.btn_add.pack(pady=10)

        ttk.Label(self, text="Search body by name").pack(pady=10)
        search_frame = ttk.Frame(self)
        search_frame.pack(padx=10, fill='x')

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_button = ttk.Button(search_frame, text="Search", command=self.search_object)
        self.search_button.pack(side='left', padx=5)

        self.search_callback = search_callback

        instr_text = (
            "Control:\n"
            "- Left click: show info about body\n"
            "- Right click: delete body\n"
            "- Space: start/stop simulation\n"
            "- Arrows: move camera\n"
            "- +/-: Scale camera"
        )
        ttk.Label(self, text=instr_text, justify='left').pack(padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.running = True

    def set_G(self):
        try:
            val = float(self.entry_G.get())
            if val <= 0:
                raise ValueError()
            self.G = val
        except ValueError:
            messagebox.showerror("Error", "Enter correct positive number of G")

    def add_body(self):
        try:
            name = self.entries["Name:"].get().strip()
            if not name:
                messagebox.showerror("Error", "Please, enter name")
                return
            x = float(self.entries["X:"].get())
            y = float(self.entries["Y:"].get())
            speed = float(self.entries["Speed:"].get())
            angle_deg = float(self.entries["Angle(deg.):"].get())
            mass = float(self.entries["Weight:"].get())
            radius = float(self.entries["Radius:"].get())
            angle_rad = math.radians(angle_deg)
            vx = speed * math.cos(angle_rad)
            vy = speed * math.sin(angle_rad)
            self.add_body_callback(x, y, vx, vy, mass, radius, name)
        except ValueError:
            messagebox.showerror("Error", "Enter correct numbers")

    def search_object(self):
        name = self.search_entry.get().strip()
        if name:
            found = self.search_callback(name)
            if not found:
                messagebox.showinfo("Search", f"Body named '{name}' not found")
        else:
            messagebox.showinfo("Search", "Please, enter name for search")

    def on_close(self):
        self.running = False
        self.destroy()
