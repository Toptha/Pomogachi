import tkinter as tk
from tkinter import ttk, messagebox, font
import sqlite3
import os

class RoundedFrame(tk.Canvas):
    def __init__(self, parent, width, height, bg_color, fg_color="#000", corner_radius=15, padding=10, **kwargs):
        super().__init__(parent, width=width, height=height, bg=bg_color, highlightthickness=0, **kwargs)
        self.corner_radius = corner_radius
        self.padding = padding
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.width = width
        self.height = height
        self.draw_rounded_rect()
        self.bind("<Configure>", lambda e: self.draw_rounded_rect())

    def draw_rounded_rect(self):
        self.delete("round_rect")
        radius = self.corner_radius
        w = self.winfo_width()
        h = self.winfo_height()
        p = self.padding
        if w < 2*radius or h < 2*radius:
            return
        self.create_arc(p, p, p+2*radius, p+2*radius, start=90, extent=90, fill=self.fg_color, outline="", tags="round_rect")
        self.create_arc(w-p-2*radius, p, w-p, p+2*radius, start=0, extent=90, fill=self.fg_color, outline="", tags="round_rect")
        self.create_arc(w-p-2*radius, h-p-2*radius, w-p, h-p, start=270, extent=90, fill=self.fg_color, outline="", tags="round_rect")
        self.create_arc(p, h-p-2*radius, p+2*radius, h-p, start=180, extent=90, fill=self.fg_color, outline="", tags="round_rect")
        self.create_rectangle(p+radius, p, w-p-radius, h-p, fill=self.fg_color, outline="", tags="round_rect")
        self.create_rectangle(p, p+radius, w-p, h-p-radius, fill=self.fg_color, outline="", tags="round_rect")

class SchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Subject Scheduler")
        self.geometry("720x650")
        self.configure(bg="#1a1a1a")
        self.resizable(False, False)

        # Fonts
        self.font_header = ("Segoe UI Variable", 22, "bold")
        self.font_label = ("Segoe UI Variable", 12)
        self.font_entry = ("Segoe UI Variable", 12)
        self.font_button = ("Segoe UI Variable", 14, "bold")
        self.font_tree = ("Segoe UI Variable", 11)

        # Colors
        self.bg_color = "#1a1a1a"
        self.card_color = "#272727"
        self.accent_color = "#ff4c4c"
        self.accent_light = "#ff6b6b"
        self.text_color = "#eee"
        self.entry_bg = "#3a3a3a"
        self.entry_fg = "#eee"
        self.button_bg = self.accent_color
        self.button_fg = "#fff"
        self.hover_bg = "#ff6666"
        self.tree_bg1 = "#2f2f2f"
        self.tree_bg2 = "#3a3a3a"
        self.tree_selected_bg = self.accent_light
        self.tree_selected_fg = "#1a1a1a"

        # Database setup
        db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'schedule.db')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT NOT NULL,
                day TEXT NOT NULL,
                time TEXT NOT NULL
            )
        """)
        self.conn.commit()

        self.valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.valid_times = ["7:30", "8:15", "9:45", "10:45", "11:45", "12:45"]

        self.max_attempts = 3
        self.attempt = 1

        self.create_widgets()
        self.load_schedule()

    def create_widgets(self):
        # Header
        header = tk.Label(self, text="Schedule a Subject", font=self.font_header, fg=self.accent_color, bg=self.bg_color)
        header.pack(pady=(30, 20))

        # Form Card (using RoundedFrame)
        self.form_card = RoundedFrame(self, width=680, height=220, bg_color=self.bg_color, fg_color=self.card_color)
        self.form_card.pack(pady=5)
        # Place Frame inside the Canvas for widgets
        self.form_frame = tk.Frame(self.form_card, bg=self.card_color)
        self.form_frame.place(relwidth=1, relheight=1)

        # Form Labels and Entries with padding
        labels = ["Your Name:", "Subject:", "Day:", "Time Slot:"]
        for i, text in enumerate(labels):
            lbl = tk.Label(self.form_frame, text=text, font=self.font_label, fg=self.text_color, bg=self.card_color, anchor="w")
            lbl.grid(row=i, column=0, sticky="w", padx=25, pady=12)

        self.name_entry = tk.Entry(self.form_frame, font=self.font_entry, bg=self.entry_bg, fg=self.entry_fg,
                                   insertbackground=self.entry_fg, relief="flat")
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=25, pady=12)

        self.subject_entry = tk.Entry(self.form_frame, font=self.font_entry, bg=self.entry_bg, fg=self.entry_fg,
                                      insertbackground=self.entry_fg, relief="flat")
        self.subject_entry.grid(row=1, column=1, sticky="ew", padx=25, pady=12)

        self.day_var = tk.StringVar(value=self.valid_days[0])
        self.day_combo = ttk.Combobox(self.form_frame, textvariable=self.day_var, state="readonly",
                                     font=self.font_entry, values=self.valid_days, width=18)
        self.day_combo.grid(row=2, column=1, sticky="ew", padx=25, pady=12)

        self.time_var = tk.StringVar(value=self.valid_times[0])
        self.time_combo = ttk.Combobox(self.form_frame, textvariable=self.time_var, state="readonly",
                                      font=self.font_entry, values=self.valid_times, width=18)
        self.time_combo.grid(row=3, column=1, sticky="ew", padx=25, pady=12)

        self.form_frame.columnconfigure(1, weight=1)

        # Submit Button with hover effect
        self.submit_btn = tk.Button(self, text="Schedule Subject", font=self.font_button, bg=self.button_bg,
                                    fg=self.button_fg, activebackground=self.hover_bg, activeforeground="#fff",
                                    relief="flat", cursor="hand2", command=self.schedule_subject)
        self.submit_btn.pack(pady=25, ipadx=15, ipady=8)
        self.submit_btn.bind("<Enter>", lambda e: self.submit_btn.config(bg=self.hover_bg))
        self.submit_btn.bind("<Leave>", lambda e: self.submit_btn.config(bg=self.button_bg))

        # Schedule Header Card
        self.schedule_label = tk.Label(self, text="Current Schedule", font=self.font_header,
                                       fg=self.accent_color, bg=self.bg_color)
        self.schedule_label.pack(pady=(10, 15))

        # Schedule Card
        self.schedule_card = RoundedFrame(self, width=680, height=320, bg_color=self.bg_color, fg_color=self.card_color)
        self.schedule_card.pack(pady=5)
        self.schedule_frame = tk.Frame(self.schedule_card, bg=self.card_color)
        self.schedule_frame.place(relwidth=1, relheight=1)

        # Treeview style override for alternating colors and selection
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("Treeview", background=self.tree_bg1, foreground=self.text_color,
                        fieldbackground=self.tree_bg1, font=self.font_tree, rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI Variable", 13, "bold"),
                        foreground=self.accent_color, background=self.card_color, relief="flat")
        style.map("Treeview", background=[('selected', self.tree_selected_bg)],
                  foreground=[('selected', self.tree_selected_fg)])

        columns = ("Name", "Subject", "Day", "Time")
        self.tree = ttk.Treeview(self.schedule_frame, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        self.tree.pack(side="left", fill="both", expand=True, padx=(20,0), pady=15)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.schedule_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y", padx=(0,20), pady=15)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Add alternating row colors manually
        self.tree.tag_configure('oddrow', background=self.tree_bg1)
        self.tree.tag_configure('evenrow', background=self.tree_bg2)

        # Bind hover effect on rows
        self.tree.bind('<Motion>', self.on_tree_hover)
        self.tree.bind('<Leave>', self.on_tree_leave)
        self.currently_hovered = None

    def on_tree_hover(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id != self.currently_hovered:
            # Remove highlight from previous row
            if self.currently_hovered:
                self.tree.tag_remove('hover', self.currently_hovered)
            # Add highlight to new row
            if row_id:
                self.tree.tag_add('hover', row_id)
                self.tree.tag_configure('hover', background=self.hover_bg)
            self.currently_hovered = row_id

    def on_tree_leave(self, event):
        if self.currently_hovered:
            self.tree.tag_remove('hover', self.currently_hovered)
            self.currently_hovered = None

    def schedule_subject(self):
        name = self.name_entry.get().strip().title()
        subject = self.subject_entry.get().strip().title()
        day = self.day_var.get()
        time = self.time_var.get()

        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        if not subject:
            messagebox.showerror("Error", "Please enter the subject to schedule.")
            return

        # Check slot availability
        self.cursor.execute("SELECT * FROM schedule WHERE day=? AND time=?", (day, time))
        if self.cursor.fetchone():
            messagebox.showwarning("Slot Occupied", f"Slot on {day} at {time} is already occupied!")
            self.attempt += 1
            if self.attempt > self.max_attempts:
                messagebox.showerror("Too Many Attempts", "Too many invalid attempts. Please try again later.")
                self.submit_btn.config(state='disabled')
            return

        self.cursor.execute("INSERT INTO schedule (name, subject, day, time) VALUES (?, ?, ?, ?)",
                            (name, subject, day, time))
        self.conn.commit()

        messagebox.showinfo("Success", f"Slot confirmed!\n\nName: {name}\nSubject: {subject}\nDay: {day}\nTime: {time}")

        self.subject_entry.delete(0, tk.END)
        self.attempt = 1
        self.load_schedule()

    def load_schedule(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.cursor.execute("SELECT name, subject, day, time FROM schedule ORDER BY day, time")
        records = self.cursor.fetchall()
        for idx, r in enumerate(records):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=r, tags=(tag,))

    def on_closing(self):
        self.conn.close()
        self.destroy()


if __name__ == "__main__":
    app = SchedulerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
