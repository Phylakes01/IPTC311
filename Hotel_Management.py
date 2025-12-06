import sys
import os
import re  # Regex for validation

# Check if running on Windows to import msvcrt for Escape key
try:
    import msvcrt
except ImportError:
    msvcrt = None  # Fallback for Mac/Linux

# Import your external modules
import Module_1 as rsvp   # Reservations
import Module_2 as guest  # Guest Profiles
import Module_3 as rooms  # Room Inventory
import Module_4 as house  # Housekeeping
import Module_5 as bill   # Billing
import Module_6 as report # Analytics

# ==========================================
# INPUT HELPER FUNCTIONS
# ==========================================

def input_with_escape(prompt):
    """
    Custom input function that detects the ESCAPE key.
    Returns the string input, or None if Escape is pressed.
    """
    if msvcrt is None:
        return input(prompt)

    print(prompt, end='', flush=True)
    buffer = []
    
    while True:
        char = msvcrt.getch()

        if char == b'\x1b':  # ESCAPE key
            print("\n🔙 [Cancelled]")
            return None
        
        elif char == b'\r':  # ENTER key
            print()
            return "".join(buffer)
        
        elif char == b'\x08':  # BACKSPACE key
            if buffer:
                buffer.pop()
                sys.stdout.write('\b \b') 
                sys.stdout.flush()
        
        else:
            try:
                decoded_char = char.decode('utf-8')
                buffer.append(decoded_char)
                sys.stdout.write(decoded_char)
                sys.stdout.flush()
            except:
                pass

def get_valid_name(prompt):
    """Validates: Only letters and spaces."""
    while True:
        val = input_with_escape(prompt)
        if val is None: return None
            
        if not val.strip():
            print("❌ Name cannot be empty.")
            continue

        if re.match(r"^[A-Za-z ]+$", val):
            return val.strip()
        else:
            print("❌ Invalid format! Please use only letters and spaces.")

def get_valid_date_input(prompt):
    """Validates: Only numbers and dashes (0-9, -)."""
    while True:
        val = input_with_escape(prompt)
        if val is None: return None
        
        if not val.strip():
            print("❌ Date cannot be empty.")
            continue

        if re.match(r"^[0-9-]+$", val):
             return val.strip()
        else:
             print("❌ Invalid characters! Please use only numbers and dashes (e.g., 2025-01-01).")

def get_valid_int(prompt):
    while True:
        val = input_with_escape(prompt)
        if val is None: return None
        try:
            return int(val)
        except ValueError:
            print("❌ Invalid input! Please enter a whole number.")

def get_valid_float(prompt):
    while True:
        val = input_with_escape(prompt)
        if val is None: return None
        try:
            return float(val)
        except ValueError:
            print("❌ Invalid input! Please enter a valid number (e.g., 100.50).")

# ==========================================
# MAIN MENU
# ==========================================

def main():
    while True:
        print("\n" + "="*40)
        print("      🏨 HOTEL MANAGEMENT SYSTEM")
        print("="*40)
        
        print("--- RESERVATIONS ---")
        print("1.  Check Availability")
        print("2.  Create Reservation")
        print("3.  Modify Reservation")
        print("4.  Cancel Reservation")
        print("5.  View Calendar")  # <-- RESTORED

        print("\n--- GUEST MANAGEMENT ---")
        print("6.  Create Guest Profile")
        print("7.  Set Preferences")     # <-- RESTORED
        print("8.  Manage Loyalty")      # <-- RESTORED
        print("9.  View Stay History")   # <-- RESTORED
        print("10. Add Guest Notes")     # <-- RESTORED
        print("11. Store Guest ID")      # <-- RESTORED

        print("\n--- ROOMS & HOUSEKEEPING ---")
        print("12. View Room Status")
        print("13. Log Damage & Auto-Charge")
        print("14. Schedule Cleaning")
        print("15. View Housekeeping Tasks")

        print("\n--- BILLING & REPORTS ---")
        print("16. View Invoice")
        print("17. Record Payment")
        print("18. View Occupancy Report")
        print("19. View Financial Report")
        print("20. 📥 Export Occupancy (CSV)")
        print("21. 📥 Export Financial (CSV)")
        print("22. Exit")

        choice = input_with_escape("\nEnter choice (1-22): ")

        if choice is None:
            print("Exiting...")
            break

        try:
            # --- RESERVATION MODULE ---
            if choice == '1':
                date = get_valid_date_input("Enter date (YYYY-MM-DD): ")
                if date: rsvp.check_room_availability(date)
            
            elif choice == '2':
                name = get_valid_name("Enter guest name: ")
                if name is None: continue 
                rtype = input_with_escape("Enter room type (room1/room2/room3): ")
                if rtype is None: continue
                date = get_valid_date_input("Enter date (YYYY-MM-DD): ")
                if date is None: continue
                rsvp.create_reservation(name, rtype, date)

            elif choice == '3':
                name = get_valid_name("Enter guest name: ")
                if name is None: continue
                new_date = get_valid_date_input("Enter new date (YYYY-MM-DD): ")
                if new_date is None: continue
                rsvp.modify_reservation(name, new_date)

            elif choice == '4':
                name = get_valid_name("Enter guest name: ")
                if name is None: continue
                rsvp.cancel_reservation(name)

            elif choice == '5':
                rsvp.view_calendar()

            # --- GUEST MODULE (Restored Features) ---
            elif choice == '6':
                name = get_valid_name("Enter guest name: ")
                if name is None: continue
                info = input_with_escape("Enter ID info: ")
                if info is None: continue
                purpose = input_with_escape("Enter travel purpose: ")
                if purpose is None: continue
                guest.manage_guest_profile({'name': name}, info, purpose)

            elif choice == '7':
                name = get_valid_name("Enter guest name: ")
                if name is None: continue
                room_pref = input_with_escape("Enter room preference: ")
                if room_pref is None: continue
                svc_pref = input_with_escape("Enter service preference: ")
                if svc_pref is None: continue
                guest.set_guest_preferences(name, room_pref, svc_pref)

            elif choice == '8':
                name = get_valid_name("Enter guest name: ")
                if name is None: continue
                action = input_with_escape("Action (add_points/set_level): ")
                if action is None: continue
                
                points = 0
                if action == "add_points":
                    p_input = get_valid_int("Enter points to add: ")
                    if p_input is None: continue
                    points = p_input
                
                guest.manage_loyalty_programs(name, action, points)

            elif choice == '9':
                name = get_valid_name("Enter guest name: ")
                if name: guest.view_stay_history(name)

            elif choice == '10':
                name = get_valid_name("Enter guest name: ")
                if name is None: continue
                note = input_with_escape("Enter note: ")
                if note: guest.add_guest_notes(name, note)

            elif choice == '11':
                name = get_valid_name("Enter guest name: ")
                if name is None: continue
                doc = input_with_escape("Enter ID Document details: ")
                if doc: guest.store_guest_id(name, doc)

            # --- ROOMS & HOUSEKEEPING ---
            elif choice == '12':
                all_rooms = rooms.get_all_rooms()
                for r in all_rooms:
                     print(f"Room {r['room_id']}: {r['status']}")

            elif choice == '13':
                print("\n--- Log Damage & Charge Guest ---")
                rid = get_valid_int("Enter Room ID: ")
                if rid is None: continue
                item = input_with_escape("Damaged item description: ")
                if item is None: continue
                cost = get_valid_float("Repair cost: ")
                if cost is None: continue

                rooms.log_damage(rid, item, cost)
                invoice = bill.get_active_invoice_by_room(rid)
                if invoice:
                    bill.add_charge(invoice["invoice_id"], f"DAMAGE: {item}", cost)
                else:
                    print("⚠️ WARNING: No active invoice found. Charge recorded in logs but not billed.")

            elif choice == '14':
                rid = get_valid_int("Enter Room ID to clean: ")
                if rid: house.schedule_cleaning(rid)

            elif choice == '15':
                house.view_housekeeping_status()

            # --- BILLING & REPORTS ---
            elif choice == '16':
                name = get_valid_name("Enter guest name: ")
                if name: bill.show_invoice(name)

            elif choice == '17':
                iid = get_valid_int("Enter Invoice ID: ")
                if iid is None: continue
                amt = get_valid_float("Amount to pay: ")
                if amt is None: continue
                method = input_with_escape("Method (Cash/Card): ")
                if method is None: continue
                bill.record_payment(iid, amt, method)

            elif choice == '18':
                report.generate_occupancy_report()

            elif choice == '19':
                report.generate_financial_report()

            elif choice == '20':
                report.export_occupancy_to_csv()
            
            elif choice == '21':
                report.export_financial_to_csv()

            elif choice == '22':
                print("Exiting...")
                break
            
            else:
                print("❌ Invalid selection.")

        except Exception as e:
            print(f"\n❌ A system error occurred: {e}")
            print("Recovering... Please try again.\n")

if __name__ == "__main__":
    main()