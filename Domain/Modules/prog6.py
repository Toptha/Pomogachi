import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'grades.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    date TEXT DEFAULT CURRENT_DATE
                )''')
    conn.commit()
    conn.close()
    load_from_db(db_path)
    return db_path


def load_from_db(db_path):
    global grades
    grades.clear()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT subject, score FROM grades ORDER BY date")
    rows = c.fetchall()
    conn.close()
    for subject, score in rows:
        grades.setdefault(subject, []).append(score)


def add_grade(db_path, subject, score):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO grades (subject, score) VALUES (?, ?)", (subject, score))
    conn.commit()
    conn.close()
    grades.setdefault(subject, []).append(score)

class GradeTrackerApp:
    def __init__(self, root, db_path):
        self.root = root
        self.db_path = db_path
        self.root.title("📊 Pomogachi - Grade Tracker")
        self.root.geometry("800x550")
        self.root.configure(bg="#1e1e2f")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#2b2b3d",
                        foreground="white",
                        rowheight=28,
                        fieldbackground="#2b2b3d",
                        font=("Segoe UI", 11))
        style.configure("Treeview.Heading",
                        background="#3b3b50",
                        foreground="white",
                        font=("Segoe UI", 12, "bold"))
        style.map("Treeview", background=[("selected", "#4a90e2")])

        input_frame = tk.Frame(root, bg="#1e1e2f", pady=15)
        input_frame.pack(fill="x")

        lbl_style = {"bg": "#1e1e2f", "fg": "white", "font": ("Segoe UI", 11)}
        tk.Label(input_frame, text="Subject:", **lbl_style).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.subject_entry = tk.Entry(input_frame, font=("Segoe UI", 11), width=15)
        self.subject_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Score:", **lbl_style).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.score_entry = tk.Entry(input_frame, font=("Segoe UI", 11), width=10)
        self.score_entry.grid(row=0, column=3, padx=5, pady=5)

        add_btn = tk.Button(input_frame,
                            text="➕ Add Grade",
                            bg="#4a90e2",
                            fg="white",
                            font=("Segoe UI", 11, "bold"),
                            relief="flat",
                            padx=10, pady=5,
                            command=self.add_grade_action)
        add_btn.grid(row=0, column=4, padx=10)

        self.tree = ttk.Treeview(root, columns=("Subject", "Score"), show="headings", height=12)
        self.tree.heading("Subject", text="Subject")
        self.tree.heading("Score", text="Score")
        self.tree.pack(fill="both", expand=True, padx=15, pady=15)

        graph_frame = tk.Frame(root, bg="#1e1e2f", pady=10)
        graph_frame.pack(fill="x")

        tk.Label(graph_frame, text="📘 Select Subject:", **lbl_style).pack(side="left", padx=5)
        self.subject_dropdown = ttk.Combobox(graph_frame, values=list(grades.keys()), font=("Segoe UI", 11))
        self.subject_dropdown.pack(side="left", padx=5)

        graph_btn = tk.Button(graph_frame,
                              text="📈 Show Progress",
                              bg="#28a745",
                              fg="white",
                              font=("Segoe UI", 11, "bold"),
                              relief="flat",
                              padx=12, pady=6,
                              command=self.show_graph)
        graph_btn.pack(side="left", padx=15)

        self.load_data()

    def add_grade_action(self):
        subject = self.subject_entry.get().strip()
        score = self.score_entry.get().strip()

        if not subject or not score.isdigit():
            messagebox.showerror("Error", "Please enter a valid subject and numeric score.")
            return

        score = int(score)
        add_grade(self.db_path, subject, score)

        self.subject_entry.delete(0, tk.END)
        self.score_entry.delete(0, tk.END)

        self.load_data()
        self.subject_dropdown['values'] = list(grades.keys())

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for subject, scores in grades.items():
            for score in scores:
                self.tree.insert("", "end", values=(subject, score))

    def show_graph(self):
        subject = self.subject_dropdown.get()
        if not subject:
            messagebox.showwarning("Select Subject", "Please select a subject first.")
            return

        scores = grades.get(subject, [])
        if not scores:
            messagebox.showinfo("No Data", f"No grades available for {subject}.")
            return


        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(range(1, len(scores)+1), scores, marker="o", color="#4a90e2")
        ax.set_facecolor("#f5f5f5")
        ax.set_title(f"Progress in {subject}", fontsize=14)
        ax.set_xlabel("Test Number")
        ax.set_ylabel("Score")

        win = tk.Toplevel(self.root)
        win.title(f"{subject} Progress Chart")
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    grades = {}
    db_path = init_db()
    root = tk.Tk()
    app = GradeTrackerApp(root, db_path)
    root.mainloop()
