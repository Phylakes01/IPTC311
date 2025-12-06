# Module_1.py: Reservation Management
from datetime import datetime
import Module_3 as rm  # Room Module
import Module_5 as bm  # Billing Module

reservations = []
waitlist = []

def validate_date_format(date_string):
    """Validates that a date string is in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def check_room_availability(date):
    print("\n--- Room Availability ---")
    try:
        if not validate_date_format(date):
            print("❌ Invalid date format. Please use YYYY-MM-DD.")
            return

        # LOGIC FIX: Check if date is in the past
        check_date = datetime.strptime(date, '%Y-%m-%d').date()
        today = datetime.now().date()

        if check_date < today:
            print(f"❌ Error: Cannot check availability for past dates ({date}).")
            print(f"   Today is: {today}")
            return

        rooms = rm.get_all_rooms()
        available_rooms = [room for room in rooms if room["status"] == "Available"]

        if not available_rooms:
            print("No rooms available on this date.")
        else:
            print(f"Availability for {date}:")
            for room in available_rooms:
                print(f"Room {room['room_id']} - {room['type']} - ₱{room['price']}")
    except Exception as e:
        print(f"❌ Error checking availability: {e}")

def create_reservation(name, room_type, check_in):
    print("\n--- Create Reservation ---")
    try:
        if not validate_date_format(check_in):
            print("❌ Invalid date format.")
            return

        # LOGIC FIX: Prevent booking in the past
        check_in_dt = datetime.strptime(check_in, '%Y-%m-%d').date()
        today = datetime.now().date()

        if check_in_dt < today:
            print("❌ Error: You cannot make a reservation for a past date.")
            return

        rooms = rm.get_all_rooms()
        
        for room in rooms:
            if room["type"].lower() == room_type.lower() and room["status"] == "Available":
                # Update Room Status in Module 3
                rm.update_room_status(room["room_id"], "Reserved")
                
                reservation = {
                    "guest": name,
                    "room_id": room["room_id"],
                    "check_in": check_in,
                    "status": "Confirmed"
                }
                reservations.append(reservation)
                
                # Auto-generate Invoice in Module 5
                try:
                    bm.create_invoice(name, room["room_id"], room["price"])
                except Exception as bill_error:
                    print(f"⚠️ Reservation made, but invoice creation failed: {bill_error}")

                print(f"✅ Reservation confirmed for {name} in Room {room['room_id']} on {check_in}")
                return

        print("ℹ️ No room available — adding to waitlist")
        waitlist.append({"guest": name, "room_type": room_type, "check_in": check_in})
        
    except Exception as e:
        print(f"❌ Error creating reservation: {e}")

def modify_reservation(guest_name, new_date):
    print("\n--- Modify Reservation ---")
    try:
        if not validate_date_format(new_date):
            print("❌ Invalid new date format.")
            return

        # LOGIC FIX: Prevent moving reservation to the past
        new_date_dt = datetime.strptime(new_date, '%Y-%m-%d').date()
        today = datetime.now().date()

        if new_date_dt < today:
            print("❌ Error: You cannot reschedule to a past date.")
            return

        for res in reservations:
            if res["guest"].lower() == guest_name.lower():
                old_date = res["check_in"]
                res["check_in"] = new_date
                print(f"✅ Reservation for {guest_name} moved from {old_date} to {new_date}")
                return
        print("❌ Reservation not found")
    except Exception as e:
        print(f"Error modifying reservation: {e}")

def cancel_reservation(guest_name):
    print("\n--- Cancel Reservation ---")
    try:
        for res in reservations:
            if res["guest"].lower() == guest_name.lower():
                room_id = res["room_id"]
                reservations.remove(res)
                
                # Set room back to available
                rm.update_room_status(room_id, "Available")

                print(f"✅ Reservation cancelled for {guest_name}")
                promote_waitlist()
                return
        print("❌ Reservation not found")
    except Exception as e:
        print(f"Error cancelling reservation: {e}")

def promote_waitlist():
    try:
        if waitlist:
            # We peek at the waitlist
            guest = waitlist[0] 
            
            # Check if waitlist date is still valid (in case days have passed)
            check_in_dt = datetime.strptime(guest["check_in"], '%Y-%m-%d').date()
            if check_in_dt < datetime.now().date():
                print(f"⚠️ Waitlist entry for {guest['guest']} is now in the past. Removing.")
                waitlist.pop(0)
                promote_waitlist() # Recursive call to check next person
                return

            waitlist.pop(0)
            create_reservation(guest["guest"], guest["room_type"], guest["check_in"])
            print(f"ℹ️ Waitlisted guest promoted: {guest['guest']}")
    except Exception as e:
        print(f"Error promoting waitlist: {e}")

def view_calendar():
    print("\n--- Calendar View ---")
    try:
        if not reservations:
            print("No reservations yet.")
        for res in reservations:
            print(f"{res['guest']} → Room {res['room_id']} on {res['check_in']}")
    except Exception as e:
        print(f"Error viewing calendar: {e}")