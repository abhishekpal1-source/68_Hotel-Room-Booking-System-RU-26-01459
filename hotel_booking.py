import json
import os

# Hotel Room Booking System
# PS No. 68
# Language: Python 3

GST_RATE = 0.12
BOOKING_FILE = "bookings.txt"

# Room details
ROOMS = {
    101: {"type": "Single", "rate": 2000},
    102: {"type": "Double", "rate": 3500},
    201: {"type": "Suite", "rate": 6000}
}


# Load bookings from file
def load_bookings():
    if not os.path.exists(BOOKING_FILE):
        return []

    try:
        with open(BOOKING_FILE, "r") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Error reading booking file.")
        return []


# Save bookings to file
def save_bookings(bookings):
    with open(BOOKING_FILE, "w") as file:
        json.dump(bookings, file, indent=4)


# Generate bill
def generate_bill(room_number, nights):
    rate = ROOMS[room_number]["rate"]

    room_charge = rate * nights
    gst = room_charge * GST_RATE
    total = room_charge + gst

    return room_charge, gst, total


# Display bill
def display_bill(room_number, nights):
    room_charge, gst, total = generate_bill(
        room_number, nights
    )

    print("\n----------- HOTEL BILL -----------")
    print("Room Number :", room_number)
    print("Room Type   :", ROOMS[room_number]["type"])
    print("Rate/Night  : Rs.", ROOMS[room_number]["rate"])
    print("Nights      :", nights)
    print("Room Charge : Rs.", room_charge)
    print("GST (12%)   : Rs.", gst)
    print("Total Bill  : Rs.", total)
    print("----------------------------------")


# Check room booking status
def is_room_booked(bookings, room_number):
    for booking in bookings:
        if booking["room_number"] == room_number:
            return True

    return False


# View available rooms
def view_available_rooms(bookings):
    print("\n-------- AVAILABLE ROOMS --------")

    found = False

    for room_number, details in ROOMS.items():

        if not is_room_booked(bookings, room_number):
            print(
                "Room:", room_number,
                "| Type:", details["type"],
                "| Rate: Rs.", details["rate"]
            )
            found = True

    if not found:
        print("No rooms available.")

    print("---------------------------------")


# Book a room
def book_room(bookings):
    print("\n---------- BOOK A ROOM ----------")

    guest_name = input("Enter guest name: ").strip()

    if not guest_name:
        print("Guest name cannot be empty.")
        return

    try:
        room_number = int(input("Enter room number: "))
    except ValueError:
        print("Invalid room number.")
        return

    if room_number not in ROOMS:
        print("Room does not exist.")
        return

    if is_room_booked(bookings, room_number):
        print("Room is already booked.")
        return

    try:
        nights = int(input("Enter number of nights: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if nights < 1 or nights > 30:
        print("Nights must be between 1 and 30.")
        return

    booking = {
        "guest_name": guest_name,
        "room_number": room_number,
        "nights": nights
    }

    bookings.append(booking)
    save_bookings(bookings)

    print("\nRoom booked successfully!")

    display_bill(room_number, nights)


# View current bookings
def view_bookings(bookings):
    print("\n---------- CURRENT BOOKINGS ----------")

    if not bookings:
        print("No bookings available.")
        return

    for index, booking in enumerate(bookings, start=1):

        room_number = booking["room_number"]

        print("\nBooking:", index)
        print("Guest Name :", booking["guest_name"])
        print("Room Number:", room_number)
        print("Room Type  :", ROOMS[room_number]["type"])
        print("Nights     :", booking["nights"])


# Cancel booking
def cancel_booking(bookings):
    print("\n---------- CANCEL BOOKING ----------")

    try:
        room_number = int(input("Enter room number: "))
    except ValueError:
        print("Invalid room number.")
        return

    for booking in bookings:

        if booking["room_number"] == room_number:

            bookings.remove(booking)
            save_bookings(bookings)

            print("Booking cancelled successfully!")
            print("Room", room_number, "is now available.")
            return

    print("No booking found for this room.")


# Display menu
def display_menu():
    print("\n====================================")
    print("     HOTEL ROOM BOOKING SYSTEM")
    print("====================================")
    print("1. View Available Rooms")
    print("2. Book a Room")
    print("3. View Current Bookings")
    print("4. Cancel a Booking")
    print("5. Exit")
    print("====================================")


# Main function
def main():

    bookings = load_bookings()

    print("\nWelcome to Hotel Room Booking System!")

    while True:

        display_menu()

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            view_available_rooms(bookings)

        elif choice == "2":
            book_room(bookings)

        elif choice == "3":
            view_bookings(bookings)

        elif choice == "4":
            cancel_booking(bookings)

        elif choice == "5":
            print("\nThank you for using our system!")
            print("Program closed successfully.")
            break

        else:
            print("Invalid choice! Please select 1 to 5.")


# Program execution
if __name__ == "__main__":
    main()