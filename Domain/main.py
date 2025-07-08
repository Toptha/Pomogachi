import tkinter as tk
import subprocess
import os

def open_scheduler():
    # Path to prog2.py
    script_path = os.path.join(os.path.dirname(__file__), 'Modules', 'prog2_GUI.py')

    # Open a new terminal window and run prog2.py
    subprocess.Popen(['python', script_path])

# Setup GUI
root = tk.Tk()
root.title("Student Scheduler")
root.geometry("300x150")

label = tk.Label(root, text="Welcome to Pomogachi!", font=("Arial", 16))
label.pack(pady=10)

btn = tk.Button(root, text="Schedule Subject", command=open_scheduler, bg="#4CAF50", fg="white", padx=10, pady=5)
btn.pack(pady=20)

root.mainloop()
