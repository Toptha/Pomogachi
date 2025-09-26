import tkinter as tk
from tkinter import ttk, messagebox

# ------------------------------
# Core Functions
# ------------------------------

def calculate_attendance(total_classes, attended_classes, required=75):
    """Calculate attendance percentage and eligibility"""
    percentage = (attended_classes / total_classes) * 100 if total_classes > 0 else 0
    status = "✅ Eligible" if percentage >= required else "❌ Not Eligible"
    return percentage, status

# Recursive: extra classes needed
def classes_needed(attended, total, required=75):
    current = (attended / total) * 100 if total > 0 else 0
    if current >= required:
        return 0
    return 1 + classes_needed(attended + 1, total + 1, required)

# Recursive: how many classes you can bunk
def bunkable_classes(attended, total, required=75):
    current = (attended / total) * 100 if total > 0 else 0
    if current < required:
        return 0
    # If after missing one class, still >= required → continue
    if ((attended) / (total + 1)) * 100 >= required:
        return 1 + bunkable_classes(attended, total + 1, required)
    return 0


# ------------------------------
# Tkinter GUI App
# ------------------------------
class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Pomogachi - Attendance Calculator")
        self.root.geometry("620x450")
        self.root.config(bg="#1e1e2f")

        # Title
        tk.Label(
            root,
            text="📊 Attendance Calculator",
            font=("Segoe UI", 22, "bold"),
            bg="#1e1e2f",
            fg="#4a90e2"
        ).pack(pady=20)

        # Form Frame
        form = tk.Frame(root, bg="#1e1e2f")
        form.pack(pady=10)

        lbl_style = {"bg": "#1e1e2f", "fg": "white", "font": ("Segoe UI", 13)}

        tk.Label(form, text="Total Classes:", **lbl_style).grid(row=0, column=0, padx=10, pady=8, sticky="e")
        tk.Label(form, text="Attended Classes:", **lbl_style).grid(row=1, column=0, padx=10, pady=8, sticky="e")
        tk.Label(form, text="Required %:", **lbl_style).grid(row=2, column=0, padx=10, pady=8, sticky="e")

        self.total_var = tk.StringVar()
        self.attended_var = tk.StringVar()
        self.required_var = tk.StringVar(value="75")

        entry_style = {"font": ("Segoe UI", 12), "width": 12}
        ttk.Entry(form, textvariable=self.total_var, **entry_style).grid(row=0, column=1, padx=10)
        ttk.Entry(form, textvariable=self.attended_var, **entry_style).grid(row=1, column=1, padx=10)
        ttk.Entry(form, textvariable=self.required_var, **entry_style).grid(row=2, column=1, padx=10)

        # Button
        ttk.Button(
            root,
            text="✨ Calculate Attendance",
            command=self.calculate,
        ).pack(pady=20)

        # Result Box
        self.result_box = tk.Label(
            root,
            text="",
            font=("Segoe UI", 13),
            bg="#1e1e2f",
            fg="white",
            justify="left"
        )
        self.result_box.pack(pady=10)

        # Style config
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        font=("Segoe UI", 12, "bold"),
                        foreground="white",
                        background="#4a90e2",
                        padding=10)
        style.map("TButton", background=[("active", "#357ABD")])

    def calculate(self):
        try:
            total = int(self.total_var.get())
            attended = int(self.attended_var.get())
            required = int(self.required_var.get())

            percentage, status = calculate_attendance(total, attended, required)
            needed = classes_needed(attended, total, required)
            can_bunk = bunkable_classes(attended, total, required)

            # Decide what to show
            extra_info = ""
            if percentage < required:
                extra_info = f"📅 Extra Classes Needed: {needed}"
            else:
                extra_info = f"😎 You can bunk {can_bunk} more classes!"

            self.result_box.config(
                text=(
                    f"📌 Attendance Report\n"
                    f"-------------------------\n"
                    f"Total Classes: {total}\n"
                    f"Attended: {attended}\n"
                    f"Required %: {required}\n\n"
                    f"📈 Current %: {percentage:.2f}%\n"
                    f"📍 Status: {status}\n"
                    f"{extra_info}"
                )
            )
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")


# ------------------------------
# Run App
# ------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
