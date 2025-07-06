import sqlite3
from datetime import datetime
import os
os.makedirs("db", exist_ok=True)
conn = sqlite3.connect("db/finance.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        note TEXT,
        date TEXT NOT NULL
    )
''')

def add_expense(amount, category, note=""):
    date =datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO expenses (amount, category, note, date)
        VALUES (?, ?, ?, ?)
    ''', (amount, category, note, date))
    conn.commit()
    print(f"Added ₹{amount} to '{category}' category.")

def view_expenses():
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows =cursor.fetchall()

    if not rows:
        print("No expenses recorded yet.")
        return

    print("\n All Expenses:")
    print("-" *70)
    print(f"{'ID':<5} {'Amount':<10} {'Category':<15} {'Note':<20} {'Date'}")
    print("-" *70)

    for row in rows:
        id, amount, category, note, date =row
        print(f"{id:<5} ₹{amount:<9.2f} {category:<15} {note[:18]:<20} {date}")
    print("-" *70)

def get_valid_amount():
    while True:
        amt_input =input("Enter amount: ₹")
        try:
            amt =float(amt_input)
            if amt <=0:
                print("Amount must be a positive number. Try again.")
            else:
                return amt
        except ValueError:
            print("Invalid input. Please enter a numeric amount.")

def get_valid_category():
    while True:
        cat =input("Enter category (e.g., food, transport): ").strip()
        if not cat:
            print("Category cannot be empty. Try again.")
        else:
            return cat.lower()

if __name__ =="__main__":
    print("Personal Finance Portfolio")

    try:
        while True:
            print("\n Expense Tracker Menu:")
            print("1. Add new expense")
            print("2. View all expenses")
            print("3. Exit")
            choice =input("Enter choice (1/2/3): ")

            if choice =="1":
                amt =get_valid_amount()
                cat =get_valid_category()
                note =input("Any note (optional): ")
                add_expense(amt, cat, note)

            elif choice =="2":
                view_expenses()

            elif choice =="3":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()
