import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# GUI
def show_message():
    messagebox.showinfo("Test", "Tkinter is working!")

root = tk.Tk()
root.title("Test")
tk.Button(root, text="Click me", command=show_message).pack()

# Matplotlib Test (on button click)
def plot_chart():
    plt.bar(["Food", "Rent", "Fun"], [2000, 5000, 1200])
    plt.title("Sample Expenses")
    plt.show()

tk.Button(root, text="Show Chart", command=plot_chart).pack()

root.mainloop()
