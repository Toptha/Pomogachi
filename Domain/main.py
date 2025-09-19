import tkinter as tk
import subprocess
import os
import sys

def open_scheduler():
    script_path = os.path.join(os.path.dirname(__file__), 'Modules', 'prog2_GUI.py')
    subprocess.Popen(['python', script_path])

def open_todo():
    script_path = os.path.join(os.path.dirname(__file__), 'Modules', 'prog3_GUI.py')
    subprocess.Popen(['python', script_path])

def open_tracker():
    script_path = os.path.join(os.path.dirname(__file__), 'Modules', 'prog6.py')
    subprocess.Popen([sys.executable, script_path])

root = tk.Tk()
root.title("Pomogachi")
root.geometry("300x150")

label = tk.Label(root, text="Welcome to Pomogachi!", font=("Arial", 16))
label.pack(pady=10)

btn = tk.Button(root, text="Schedule Subject", command=open_scheduler, bg="#4CAF50", fg="white", padx=10, pady=5)
btn.pack(pady=20)

btn_todo = tk.Button(root, text="To-Do List", command=open_todo, bg="#2196F3", fg="white", padx=10, pady=5)
btn_todo.pack(pady=20)

btn_tracker = tk.Button(root, text="Grade Tracker", command=open_tracker, bg="#800000", fg="white", padx=10, pady=5)
btn_tracker.pack(pady=20)

root.mainloop()
