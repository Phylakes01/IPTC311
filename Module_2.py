guests = []

def manage_guest_profile(contact_info, id_info, travel_purpose):
    print("\n--- Guest Profile Management ---")
    try:
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
        print(f"✅ Guest profile created for {contact_info.get('name', 'Unknown')}.")
    except Exception as e:
        print(f"❌ Error creating profile: {e}")

def find_guest(guest_name):
    try:
        for guest in guests:
            if guest["contact_info"]["name"].lower() == guest_name.lower():
                return guest
    except KeyError:
        return None
    return None

def set_guest_preferences(guest_name, room_preference, service_preference):
    try:
        guest = find_guest(guest_name)
        if guest:
            guest["preferences"]["room"] = room_preference
            guest["preferences"]["service"] = service_preference
            print(f"✅ Preferences updated for {guest_name}.")
        else:
            print("❌ Guest not found.")
    except Exception as e:
        print(f"Error setting preferences: {e}")

def manage_loyalty_programs(guest_name, action, points=0):
    try:
        guest = find_guest(guest_name)
        if guest:
            if action == "add_points":
                if not isinstance(points, (int, float)):
                     print("❌ Points must be a number.")
                     return
                guest["loyalty"]["points"] += points
                print(f"✅ {points} points added. Total: {guest['loyalty']['points']}")
            elif action == "set_level":
                level = input("Enter new loyalty level: ")
                guest["loyalty"]["level"] = level
                print(f"✅ Loyalty level updated to {level}.")
        else:
            print("❌ Guest not found.")
    except Exception as e:
        print(f"Error managing loyalty: {e}")

def view_stay_history(guest_name):
    try:
        guest = find_guest(guest_name)
        if guest:
            print(f"\n--- Stay History for {guest_name} ---")
            if not guest["stay_history"]:
                print("No past stays recorded.")
            for stay in guest["stay_history"]:
                print(stay)
        else:
            print("❌ Guest not found.")
    except Exception as e:
        print(f"Error viewing history: {e}")

def add_guest_notes(guest_name, note):
    try:
        guest = find_guest(guest_name)
        if guest:
            guest["notes"] = note
            print(f"✅ Note added for {guest_name}.")
        else:
            print("❌ Guest not found.")
    except Exception as e:
        print(f"Error adding note: {e}")

def store_guest_id(guest_name, id_document):
    try:
        guest = find_guest(guest_name)
        if guest:
            guest["id_storage"] = id_document
            print(f"✅ ID stored for {guest_name}.")
        else:
            print("❌ Guest not found.")
    except Exception as e:
        print(f"Error storing ID: {e}")