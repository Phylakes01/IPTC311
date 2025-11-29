guests = []

def manage_guest_profile(contact_info, id_info, travel_purpose):
    print("\nGuest Profile Management")
    guest = {
        "contact_info": contact_info,
        "id_info": id_info,
        "travel_purpose": travel_purpose,
        "preferences": {},
        "loyalty": {"level": "Bronze", "points": 0},
        "stay_history": [],
        "notes": ""
    }
    guests.append(guest)
    print(f"Guest profile created for {contact_info['name']}.")

def find_guest(guest_name):
    """Finds a guest by name."""
    for guest in guests:
        if guest["contact_info"]["name"].lower() == guest_name.lower():
            return guest
    return None

def set_guest_preferences(guest_name, room_preference, service_preference):
    guest = find_guest(guest_name)
    if guest:
        guest["preferences"]["room"] = room_preference
        guest["preferences"]["service"] = service_preference
        print(f"Preferences updated for {guest_name}.")
    else:
        print("Guest not found.")

def manage_loyalty_programs(guest_name, action, points=0):
    guest = find_guest(guest_name)
    if guest:
        if action == "add_points":
            guest["loyalty"]["points"] += points
            print(f"{points} points added to {guest_name}'s loyalty account.")
        elif action == "set_level":
            level = input("Enter new loyalty level: ")
            guest["loyalty"]["level"] = level
            print(f"Loyalty level for {guest_name} updated to {level}.")
    else:
        print("Guest not found.")

def view_stay_history(guest_name):
    guest = find_guest(guest_name)
    if guest:
        print(f"\n--- Stay History for {guest_name} ---")
        if not guest["stay_history"]:
            print("No past stays.")
        for stay in guest["stay_history"]:
            print(stay)
    else:
        print("Guest not found.")

def add_guest_notes(guest_name, note):
    guest = find_guest(guest_name)
    if guest:
        guest["notes"] = note
        print(f"Note added for {guest_name}.")
    else:
        print("Guest not found.")

def store_guest_id(guest_name, id_document):
    guest = find_guest(guest_name)
    if guest:
        guest["id_storage"] = id_document
        print(f"ID stored for {guest_name}.")
    else:
        print("Guest not found.")