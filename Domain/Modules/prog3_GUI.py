import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

TASKS_CSV = os.path.join(os.path.dirname(__file__), '..', 'db', 'tasks.csv')
tasks = []

class HoverButton(tk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.default_bg = kw.get('bg', '#ff6b6b')
        self.hover_bg = kw.get('activebackground', '#ff8787')
        self['relief'] = 'flat'
        self['bd'] = 0
        self['cursor'] = 'hand2'
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self.hover_bg

    def on_leave(self, e):
        self['background'] = self.default_bg

class TaskManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Task Manager")
        self.geometry("780x520")
        self.configure(bg="#121212")
        self.resizable(True, True)

        # Style config
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure("Treeview",
                             background="#1e1e1e",
                             foreground="white",
                             fieldbackground="#1e1e1e",
                             font=("Segoe UI", 11),
                             rowheight=28,
                             bordercolor="#222222",
                             borderwidth=0)
        self.style.configure("Treeview.Heading",
                             font=("Segoe UI Semibold", 14),
                             foreground="#ff6b6b",
                             background="#121212",
                             relief="flat")
        self.style.map("Treeview",
                       background=[('selected', '#ff6b6b')],
                       foreground=[('selected', '#121212')])

        self.create_widgets()
        self.load_tasks()
        self.populate_treeview()

    def create_widgets(self):
        # Filter Frame
        filter_frame = tk.Frame(self, bg="#121212")
        filter_frame.pack(fill="x", pady=(15,5), padx=15)

        tk.Label(filter_frame, text="Filter Tasks:",
                 fg="#bbb", bg="#121212", font=("Segoe UI", 13)).pack(side="left")

        self.filter_var = tk.StringVar(value="All")
        self.filter_combo = ttk.Combobox(filter_frame, values=["All", "Pending", "Finished"],
                                         textvariable=self.filter_var,
                                         state="readonly", width=12,
                                         font=("Segoe UI", 12, "bold"))
        self.filter_combo.pack(side="left", padx=10)
        self.filter_combo.bind("<<ComboboxSelected>>", lambda e: self.populate_treeview())

        # Treeview
        columns = ("Task", "Deadline", "Priority", "Progress")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=170)

        self.tree.pack(fill="both", expand=True, padx=15, pady=10)
        self.tree.tag_configure("oddrow", background="#232323")
        self.tree.tag_configure("evenrow", background="#1b1b1b")

        # Hover effect on rows
        self.tree.bind('<Motion>', self.on_tree_hover)
        self.tree.bind('<Leave>', self.on_tree_leave)
        self.currently_hovered = None

        # Buttons Frame
        btn_frame = tk.Frame(self, bg="#121212")
        btn_frame.pack(fill="x", padx=15, pady=(0,15))

        buttons = [
            ("Add Task", self.add_task),
            ("Mark Finished", self.mark_finished),
            ("Remove Task", self.remove_task),
            ("Sort by Deadline", self.sort_by_deadline),
            ("Count Tasks", self.count_tasks_by_status),
            ("Find Task Index", self.find_task_index),
            ("Top 3 Pending", self.show_top_3_tasks),
            ("Clear All", self.clear_all_tasks),
            ("Save & Exit", self.save_and_exit)
        ]

        for text, cmd in buttons:
            btn = HoverButton(btn_frame, text=text, command=cmd,
                              bg="#ff6b6b", activebackground="#ff8787",
                              fg="#121212", font=("Segoe UI Semibold", 12),
                              padx=12, pady=8)
            btn.pack(side="left", padx=6, pady=5)

        # Status bar
        self.status_var = tk.StringVar(value="Welcome to your dope Task Manager!")
        self.status_bar = tk.Label(self, textvariable=self.status_var, fg="#ff6b6b", bg="#121212",
                                   font=("Segoe UI", 11), anchor="w")
        self.status_bar.pack(fill="x", side="bottom", ipady=6, padx=10)

    def on_tree_hover(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id != self.currently_hovered:
            if self.currently_hovered:
                self.tree.tag_remove('hover', self.currently_hovered)
            if row_id:
                self.tree.tag_add('hover', row_id)
                self.tree.tag_configure('hover', background="#ff4c4c")
            self.currently_hovered = row_id

    def on_tree_leave(self, event):
        if self.currently_hovered:
            self.tree.tag_remove('hover', self.currently_hovered)
            self.currently_hovered = None

    def load_tasks(self):
        tasks.clear()
        if not os.path.exists(TASKS_CSV):
            os.makedirs(os.path.dirname(TASKS_CSV), exist_ok=True)
            with open(TASKS_CSV, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Task", "Deadline", "Priority", "Progress"])
        else:
            with open(TASKS_CSV, 'r') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) == 4:
                        tasks.append(row)

    def save_tasks(self):
        with open(TASKS_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Task", "Deadline", "Priority", "Progress"])
            writer.writerows(tasks)
        self.status_var.set("Tasks saved successfully.")

    def populate_treeview(self):
        filter_by = self.filter_var.get()
        self.tree.delete(*self.tree.get_children())
        filtered = tasks
        if filter_by in ("Pending", "Finished"):
            filtered = [t for t in tasks if t[3] == filter_by]

        for i, task in enumerate(filtered):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert('', 'end', values=task, tags=(tag,))

        if not filtered:
            self.status_var.set(f"No tasks to show ({filter_by})")
        else:
            self.status_var.set(f"Showing {len(filtered)} tasks ({filter_by})")

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter task name:", parent=self)
        if not task or not task.strip():
            self.status_var.set("Add task cancelled or empty task.")
            return

        deadline = simpledialog.askstring("Add Task", "Enter deadline (YYYY-MM-DD):", parent=self)
        if not deadline:
            self.status_var.set("Add task cancelled or no deadline entered.")
            return
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Deadline must be in YYYY-MM-DD format.", parent=self)
            return

        priority = simpledialog.askstring("Add Task", "Enter priority (High/Medium/Low):", parent=self)
        if priority is None:
            self.status_var.set("Add task cancelled or no priority entered.")
            return
        priority = priority.capitalize()
        if priority not in ("High", "Medium", "Low"):
            messagebox.showerror("Invalid Priority", "Priority must be High, Medium, or Low.", parent=self)
            return

        tasks.append([task.strip(), deadline.strip(), priority, "Pending"])
        self.populate_treeview()
        self.status_var.set(f"Task '{task}' added.")

    def mark_finished(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Select a task to mark as finished.", parent=self)
            return
        values = self.tree.item(selected, 'values')
        task_name = values[0]

        for task in tasks:
            if task[0].lower() == task_name.lower():
                if task[3] == "Finished":
                    messagebox.showinfo("Already Finished", f"Task '{task_name}' is already marked finished.", parent=self)
                    return
                task[3] = "Finished"
                self.populate_treeview()
                self.status_var.set(f"Task '{task_name}' marked as Finished.")
                return

        messagebox.showerror("Task Not Found", "Selected task was not found.", parent=self)

    def remove_task(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Select a task to remove.", parent=self)
            return
        values = self.tree.item(selected, 'values')
        task_name = values[0]

        if messagebox.askyesno("Confirm Delete", f"Remove task '{task_name}'?", parent=self):
            for task in tasks:
                if task[0].lower() == task_name.lower():
                    tasks.remove(task)
                    self.populate_treeview()
                    self.status_var.set(f"Task '{task_name}' removed.")
                    return
            messagebox.showerror("Task Not Found", "Selected task was not found.", parent=self)

    def sort_by_deadline(self):
        try:
            tasks.sort(key=lambda x: datetime.strptime(x[1], "%Y-%m-%d"))
            self.populate_treeview()
            self.status_var.set("Tasks sorted by deadline.")
        except Exception as e:
            messagebox.showerror("Error", f"Sorting error: {e}", parent=self)

    def clear_all_tasks(self):
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all tasks?", parent=self):
            tasks.clear()
            self.populate_treeview()
            self.status_var.set("All tasks cleared.")

    def count_tasks_by_status(self):
        pending = sum(1 for t in tasks if t[3] == "Pending")
        finished = sum(1 for t in tasks if t[3] == "Finished")
        messagebox.showinfo("Task Counts", f"Pending: {pending}\nFinished: {finished}\nTotal: {len(tasks)}", parent=self)
        self.status_var.set("Displayed task counts.")

    def find_task_index(self):
        name = simpledialog.askstring("Find Task", "Enter task name to find:", parent=self)
        if not name:
            self.status_var.set("Find task cancelled.")
            return
        for idx, task in enumerate(tasks):
            if task[0].lower() == name.lower():
                messagebox.showinfo("Task Found", f"Task '{task[0]}' found at index {idx}.", parent=self)
                self.status_var.set(f"Task '{task[0]}' found at index {idx}.")
                return
        messagebox.showinfo("Not Found", f"Task '{name}' not found.", parent=self)
        self.status_var.set(f"Task '{name}' not found.")

    def show_top_3_tasks(self):
        upcoming = sorted([t for t in tasks if t[3] == "Pending"],
                          key=lambda x: datetime.strptime(x[1], "%Y-%m-%d"))[:3]
        if upcoming:
            msg = "\n".join(f"- {t[0]} (Due: {t[1]}, Priority: {t[2]})" for t in upcoming)
            messagebox.showinfo("Top 3 Upcoming Pending Tasks", msg, parent=self)
            self.status_var.set("Displayed top 3 pending tasks.")
        else:
            messagebox.showinfo("No Pending Tasks", "No pending tasks found.", parent=self)
            self.status_var.set("No pending tasks.")

    def save_and_exit(self):
        self.save_tasks()
        self.destroy()

if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()
