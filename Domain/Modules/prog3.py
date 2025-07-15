import csv
import os
from datetime import datetime

TASKS_CSV =os.path.join(os.path.dirname(__file__), '..', 'db', 'tasks.csv')
tasks =[]  

def load_tasks():
    tasks.clear()
    if not os.path.exists(TASKS_CSV):
        with open(TASKS_CSV, 'w', newline='') as f:
            writer =csv.writer(f)
            writer.writerow(["Task", "Deadline", "Priority", "Progress"])
    else:
        with open(TASKS_CSV, 'r') as f:
            reader =csv.reader(f)
            next(reader, None) 
            for row in reader:
                if len(row) ==4:
                    tasks.append(row)

def save_tasks():
    with open(TASKS_CSV, 'w', newline='') as f:
        writer =csv.writer(f)
        writer.writerow(["Task", "Deadline", "Priority", "Progress"])
        writer.writerows(tasks)

def add_task():
    task =input("Enter task name: ").strip()
    deadline =input("Enter deadline (YYYY-MM-DD): ").strip()
    priority =input("Enter priority (High/Medium/Low): ").strip().capitalize()

    try:
        datetime.strptime(deadline, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format.")
        return

    tasks.append([task, deadline, priority, "Pending"])
    print("Task added.")

def view_tasks(filter_by=None):
    filtered =tasks
    if filter_by in ("Pending", "Finished"):
        filtered =[t for t in tasks if t[3] ==filter_by]

    if not filtered:
        print("No tasks to show.")
        return

    print(f"\n{'Task':<25}{'Deadline':<15}{'Priority':<10}{'Progress':<10}")
    print("-"*65)
    for task in filtered:
        print(f"{task[0]:<25}{task[1]:<15}{task[2]:<10}{task[3]:<10}")

def mark_finished():
    task_name =input("Enter exact task name to mark as Finished: ").strip()
    for task in tasks:
        if task[0].lower() ==task_name.lower():
            if task[3] =="Finished":
                print("Already marked as finished.")
            else:
                task[3] ="Finished"
                print("Marked as Finished.")
            return
    print("Task not found.")

def remove_task():
    task_name =input("Enter task name to remove: ").strip()
    for task in tasks:
        if task[0].lower() ==task_name.lower():
            tasks.remove(task)
            print(" Task removed.")
            return
    print("Task not found.")

def sort_by_deadline():
    try:
        tasks.sort(key=lambda x: datetime.strptime(x[1], "%d-%m-%Y"))
        print("Tasks sorted by deadline.")
    except Exception as e:
        print(f"Error: {e}")

def clear_all_tasks():
    if input("Are you sure? (y/n): ").lower() =='y':
        tasks.clear()
        print("All tasks cleared.")

def count_tasks_by_status():
    pending =sum(1 for t in tasks if t[3] =="Pending")
    finished =sum(1 for t in tasks if t[3] =="Finished")
    print(f"Pending: {pending} | Finished: {finished} | Total: {len(tasks)}")

def find_task_index():
    name =input("Enter task name to find: ").strip()
    for idx, task in enumerate(tasks):
        if task[0].lower() ==name.lower():
            print(f"Task '{task[0]}' found at index {idx}")
            return
    print("Task not found.")

def show_top_3_tasks():
    upcoming =sorted(
        [t for t in tasks if t[3] =="Pending"],
        key=lambda x: datetime.strptime(x[1], "%d-%m-%Y")
    )[:3]
    if upcoming:
        print("\nTop 3 Upcoming Pending Tasks:")
        for t in upcoming:
            print(f"- {t[0]} (Due: {t[1]}, Priority: {t[2]})")
    else:
        print("No pending tasks.")

def menu():
    load_tasks()
    while True:
        print("\n=== Program 3 ===")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. View Finished Tasks")
        print("5. Mark Task as Finished")
        print("6. Remove Task")
        print("7. Sort by Deadline")
        print("8. Count Tasks by Status")
        print("9. Find Task Index")
        print("10. Show Top 3 Pending Tasks")
        print("11. Save & Exit")
        choice =input("Choose: ")

        match choice:
            case '1': add_task()
            case '2': view_tasks()
            case '3': view_tasks("Pending")
            case '4': view_tasks("Finished")
            case '5': mark_finished()
            case '6': remove_task()
            case '7': sort_by_deadline()
            case '8': count_tasks_by_status()
            case '9': find_task_index()
            case '10': show_top_3_tasks()
            case '11':
                save_tasks()
                print("Saved and exiting...")
                break
            case _: print("Invalid option.")

if __name__ =="__main__":
    menu()
