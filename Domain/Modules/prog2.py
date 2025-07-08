import sqlite3
import os

print("=== Program 2 ===")
print("You can schedule 1 subject into a valid time slot.\n")
print("Valid Days: Monday, Tuesday, Wednesday, Thursday, Friday")
print("Valid Time Slots: 7:30, 8:15, 9:45, 10:45, 11:45, 12:45")

db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'schedule.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        subject TEXT NOT NULL,
        day TEXT NOT NULL,
        time TEXT NOT NULL
    )
""")
conn.commit()

valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
valid_times = ["7:30", "8:15", "9:45", "10:45", "11:45", "12:45"]

max_attempts = 3
attempt = 1

name = input("Enter your name: ").strip().title()

while attempt <= max_attempts:
    subject = input("Enter the subject to schedule: ").strip().title()
    day = input("Enter the day: ").strip().capitalize()
    time = input("Enter the time slot (7:30, 8:15, 9:45, 10:45, 11:45, 12:45): ").strip()

    if day not in valid_days:
        print("Invalid day. Please enter a weekday (Mon–Fri).")
        attempt += 1
        continue

    if time not in valid_times:
        print("Invalid time slot.")
        attempt += 1
        continue

    cursor.execute("SELECT * FROM schedule WHERE day=? AND time=?", (day, time))
    if cursor.fetchone():
        print(f"Slot on {day} at {time} is already occupied! Please choose a different time.")
        attempt += 1
        continue

    cursor.execute("INSERT INTO schedule (name, subject, day, time) VALUES (?, ?, ?, ?)",
                   (name, subject, day, time))
    conn.commit()

    print("\nSlot confirmed!")
    print(f"Name: {name}")
    print(f"Subject: {subject}")
    print(f"Day: {day}")
    print(f"Time: {time}")
    print("Exiting...")
    break

if attempt > max_attempts:
    print("\nToo many invalid attempts. Please try again later.")

print("\n=== Current Schedule ===")
cursor.execute("SELECT name, subject, day, time FROM schedule ORDER BY day, time")
records = cursor.fetchall()

if records:
    for row in records:
        print(f"{row[0]:<15} | {row[1]:<20} | {row[2]:<10} | {row[3]}")
else:
    print("No records scheduled yet.")

conn.close()
