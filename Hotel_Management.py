from datetime import datetime
import Module_2 as cm

rooms = [
    {"room_id": 101, "type": "room1", "price": 100,  "status": "Available"},
    {"room_id": 102, "type": "room2", "price": 200,  "status": "Available"},
    {"room_id": 103, "type": "room3", "price": 300,  "status": "Available"}
]

reservations = []
waitlist = []


def validate_date(date_string):
    """Validates that a date string is in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def check_room_availability(date):
    print("\nRoom Available")
    available_rooms = [room for room in rooms if room["status"] == "Available"]

    if not available_rooms:
        print("No rooms available on this date.")
    else:
        for room in available_rooms:
            print(f"Room {room['room_id']} - {room['type']} - ₱{room['price']}")


def create_reservation(name, room_type, check_in):
    print("\nCreate Reservation")
    for room in rooms:
        if room["type"].lower() == room_type.lower() and room["status"] == "Available":
            room["status"] = "Reserved"
            reservation = {
                "guest": name,
                "room_id": room["room_id"],
                "check_in": check_in,
                "status": "Confirmed"
            }
            reservations.append(reservation)
            print(f"Reservation confirmed for {name} in Room {room['room_id']}")
            return

    print("No room available — adding to waitlist")
    waitlist.append({"guest": name, "room_type": room_type, "check_in": check_in})


def modify_reservation(guest_name, new_date):
    print("\nModify Reservation")
    for res in reservations:
        if res["guest"].lower() == guest_name.lower():
            res["check_in"] = new_date
            print(f"Reservation updated for {guest_name}")
            return
    print("Reservation not found")


def cancel_reservation(guest_name):
    print("\nCancel Reservation")
    for res in reservations:
        if res["guest"].lower() == guest_name.lower():
            room_id = res["room_id"]
            reservations.remove(res)

            for room in rooms:
                if room["room_id"] == room_id:
                    room["status"] = "Available"
                    break

            print(f"Reservation cancelled for {guest_name}")
            promote_waitlist()
            return
    print("Reservation not found")


def promote_waitlist():
    if waitlist:
        guest = waitlist.pop(0)
        create_reservation(guest["guest"], guest["room_type"], guest["check_in"])
        print(f"Waitlisted guest promoted: {guest['guest']}")


def view_calendar():
    print("\n--- Calendar View ---")
    if not reservations:
        print("No reservations yet.")
    for res in reservations:
        print(f"{res['guest']} → Room {res['room_id']} on {res['check_in']}")


def main():
    while True:
        print("\n--- Hotel Management System ---")
        print("1. Check Room Availability")
        print("2. Create Reservation")
        print("3. Modify Reservation")
        print("4. Cancel Reservation")
        print("5. View Calendar")
        print("6. Manage Guest Profile")
        print("7. Set Guest Preferences")
        print("8. Manage Loyalty Programs")
        print("9. View Stay History")
        print("10. Add Guest Notes")
        print("11. Store Guest ID")
        print("12. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            if not validate_date(date):
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            check_room_availability(date)
        elif choice == '2':
            name = input("Enter guest name: ")
            if not name.strip():
                print("Guest name cannot be empty.")
                continue
            room_type = input("Enter room type (room1, room2, room3): ")
            if room_type not in [r['type'] for r in rooms]:
                print("Invalid room type.")
                continue
            check_in = input("Enter check-in date (YYYY-MM-DD): ")
            if not validate_date(check_in):
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            create_reservation(name, room_type, check_in)
        elif choice == '3':
            name = input("Enter guest name: ")
            if not name.strip():
                print("Guest name cannot be empty.")
                continue
            new_date = input("Enter new check-in date (YYYY-MM-DD): ")
            if not validate_date(new_date):
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            modify_reservation(name, new_date)
        elif choice == '4':
            name = input("Enter guest name: ")
            if not name.strip():
                print("Guest name cannot be empty.")
                continue
            cancel_reservation(name)
        elif choice == '5':
            view_calendar()
        elif choice == '6':
            name = input("Enter guest name: ")
            if not name.strip():
                print("Guest name cannot be empty.")
                continue
            contact_info = {'name': name}
            id_info = input("Enter ID info: ")
            travel_purpose = input("Enter travel purpose: ")
            cm.manage_guest_profile(contact_info, id_info, travel_purpose)
        elif choice == '7':
            name = input("Enter guest name: ")
            if not name.strip():
                print("Guest name cannot be empty.")
                continue
            room_pref = input("Enter room preference: ")
            service_pref = input("Enter service preference: ")
            cm.set_guest_preferences(name, room_pref, service_pref)
        elif choice == '8':
            name = input("Enter guest name: ")
            if not name.strip():
                print("Guest name cannot be empty.")
                continue
            action = input("Enter action (add_points/set_level): ")
            if action not in ["add_points", "set_level"]:
                print("Invalid action.")
                continue
            points = 0
            if action == "add_points":
                try:
                    points = int(input("Enter points to add: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
            cm.manage_loyalty_programs(name, action, points)
        elif choice == '9':
            name = input("Enter guest name: ")
            if not name.strip():
                print("Guest name cannot be empty.")
                continue
            cm.view_stay_history(name)
        elif choice == '10':
            name = input("Enter guest name: ")
            if not name.strip():
                print("Guest name cannot be empty.")
                continue
            note = input("Enter note: ")
            cm.add_guest_notes(name, note)
        elif choice == '11':
            name = input("Enter guest name: ")
            if not name.strip():
                print("Guest name cannot be empty.")
                continue
            id_doc = input("Enter ID document details: ")
            cm.store_guest_id(name, id_doc)
        elif choice == '12':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()