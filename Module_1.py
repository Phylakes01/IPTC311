from datetime import datetime

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