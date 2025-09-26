import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys
import ttkbootstrap as tb  

def open_scheduler():
    script_path = os.path.join(os.path.dirname(__file__), 'Modules', 'prog2_GUI.py')
    subprocess.Popen([sys.executable, script_path])

def open_todo():
    script_path = os.path.join(os.path.dirname(__file__), 'Modules', 'prog3_GUI.py')
    subprocess.Popen([sys.executable, script_path])

def open_tracker():
    script_path = os.path.join(os.path.dirname(__file__), 'Modules', 'prog6.py')
    subprocess.Popen([sys.executable, script_path])

def open_budget():
    script_path = os.path.join(os.path.dirname(__file__), 'Modules', 'prog7.py')
    subprocess.Popen([sys.executable, script_path])

def open_attendance():
    script_path = os.path.join(os.path.dirname(__file__), 'Modules', 'prog8.py')
    subprocess.Popen([sys.executable, script_path])

root = tb.Window(themename="cyborg")  
root.title("Pomogachi")
root.geometry("600x500")

title = ttk.Label(root, text="🚀 Welcome to Pomogachi 🚀", font=("Arial Rounded MT Bold", 22))
title.pack(pady=20)

card_frame = ttk.Frame(root)
card_frame.pack(expand=True, fill="both", padx=20, pady=20)

def create_card(parent, title, emoji, command, color):
    card = ttk.Frame(parent, style="Card.TFrame", padding=20)
    card.pack(pady=15, fill="x")

    lbl = ttk.Label(card, text=f"{emoji} {title}", font=("Arial Rounded MT Bold", 16))
    lbl.pack(side="left")

    btn = ttk.Button(card, text="Open", bootstyle=color, command=command)
    btn.pack(side="right")

create_card(card_frame, "Schedule Subject", "📅", open_scheduler, "success")
create_card(card_frame, "To-Do List", "📝", open_todo, "info")
create_card(card_frame, "Grade Tracker", "📊", open_tracker, "danger")
create_card(card_frame, "Budget Tracker", "💰", open_budget, "warning")
create_card(card_frame, "Attendance Calculator", "🎓", open_attendance, "purple")

root.mainloop()
