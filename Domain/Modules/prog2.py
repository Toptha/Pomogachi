# Domain : Smart Scheduler
print("===Program 2 ===")
print("You can schedule 1 subject into a valid time slot.\n")
print("Valid Days: Monday, Tuesday, Wednesday, Thursday, Friday")
print("Valid Time Slots: 9AM, 10AM, 11AM")
occupied_day ="Wednesday"
occupied_time ="10AM"
max_attempts =3
attempt =1
while attempt <=max_attempts:
    subject =input("Enter the subject to schedule: ").strip().title()
    day =input("Enter the day: ").strip().capitalize()
    time =input("Enter the time slot (9AM, 10AM, 11AM): ").strip().upper()
    if day !="Monday" and day !="Tuesday" and day !="Wednesday" and day !="Thursday" and day !="Friday":
        print("Invalid day. Please enter a weekday (Mon–Fri).")
        attempt +=1
        continue
    if time !="9AM" and time !="10AM" and time !="11AM":
        print("Invalid time slot. Please enter 9AM, 10AM, or 11AM.")
        attempt +=1
        continue
    if day ==occupied_day and time ==occupied_time:
        print(f"Slot on {day} at {time} is already occupied! Please choose a different time.")
        attempt +=1
        continue
    print("\nSlot confirmed!")
    print(f"Subject: {subject}")
    print(f"Day: {day}")
    print(f"Time: {time}")
    print("Exiting...")
    break
if attempt >max_attempts:
    print("\nToo many invalid attempts. Please try again later.")
