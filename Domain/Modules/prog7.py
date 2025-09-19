import tkinter as tk
from tkinter import ttk, messagebox

class BudgetTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Pomogachi - Budget Tracker")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e2f")

        self.expenses = [] 
        input_frame = tk.Frame(root, bg="#1e1e2f", pady=15)
        input_frame.pack(fill="x")

        lbl_style = {"bg": "#1e1e2f", "fg": "white", "font": ("Segoe UI", 11)}

        tk.Label(input_frame, text="Amount:", **lbl_style).grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(input_frame, font=("Segoe UI", 11), width=10)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Category:", **lbl_style).grid(row=0, column=2, padx=5, pady=5)
        self.category_entry = tk.Entry(input_frame, font=("Segoe UI", 11), width=15)
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Note:", **lbl_style).grid(row=0, column=4, padx=5, pady=5)
        self.note_entry = tk.Entry(input_frame, font=("Segoe UI", 11), width=20)
        self.note_entry.grid(row=0, column=5, padx=5, pady=5)

        add_btn = tk.Button(input_frame,
                            text="➕ Add Expense",
                            bg="#4a90e2", fg="white",
                            font=("Segoe UI", 11, "bold"),
                            relief="flat", padx=10, pady=5,
                            command=self.add_expense)
        add_btn.grid(row=0, column=6, padx=10)

        self.tree = ttk.Treeview(root, columns=("Amount", "Category", "Note"), show="headings", height=12)
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Note", text="Note")
        self.tree.pack(fill="both", expand=True, padx=15, pady=15)

        btn_frame = tk.Frame(root, bg="#1e1e2f", pady=10)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="📋 Show All Amounts", bg="#17a2b8", fg="white",
                  font=("Segoe UI", 11, "bold"), relief="flat", padx=10, pady=5,
                  command=self.show_amounts).pack(side="left", padx=10)

        tk.Button(btn_frame, text="🗂 Unique Categories", bg="#ffc107", fg="black",
                  font=("Segoe UI", 11, "bold"), relief="flat", padx=10, pady=5,
                  command=self.show_categories).pack(side="left", padx=10)

        tk.Button(btn_frame, text="📊 Totals per Category", bg="#28a745", fg="white",
                  font=("Segoe UI", 11, "bold"), relief="flat", padx=10, pady=5,
                  command=self.show_totals).pack(side="left", padx=10)

    def add_expense(self):
        amount = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        note = self.note_entry.get().strip()

        if not amount.isdigit() or not category:
            messagebox.showerror("Error", "Enter a valid numeric amount and a category.")
            return

        expense = {"amount": int(amount), "category": category, "note": note}
        self.expenses.append(expense)

        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)

        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for exp in self.expenses:
            self.tree.insert("", "end", values=(exp["amount"], exp["category"], exp["note"]))

    def show_amounts(self):
        amounts = [exp["amount"] for exp in self.expenses]
        messagebox.showinfo("All Amounts", f"💵 {amounts}")

    def show_categories(self):
        categories = {exp["category"] for exp in self.expenses}
        messagebox.showinfo("Unique Categories", f"🗂 {categories}")

    def show_totals(self):
        categories = {exp["category"] for exp in self.expenses}
        totals = {cat: sum(exp["amount"] for exp in self.expenses if exp["category"] == cat)
                  for cat in categories}
        messagebox.showinfo("Totals Per Category", f"📊 {totals}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()
