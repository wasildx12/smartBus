"""
Smart Bus Ticket Booking & Reservation System
A console application using only built-in Python 3 features.
All data is kept in memory and is lost when the program exits.
"""

# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------

# Tuple: supported cities (used for the schedule report)
SUPPORTED_CITIES = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")

# List of dictionaries: bus routes
routes = [
    {"route_id": "R101", "departure_city": "Karachi", "destination_city": "Hyderabad",
     "departure_time": "08:00 AM", "ticket_price": 1200, "total_seats": 40, "available_seats": 40},
    {"route_id": "R102", "departure_city": "Karachi", "destination_city": "Sukkur",
     "departure_time": "09:30 AM", "ticket_price": 2000, "total_seats": 36, "available_seats": 36},
    {"route_id": "R103", "departure_city": "Hyderabad", "destination_city": "Mirpur Khas",
     "departure_time": "11:00 AM", "ticket_price": 800, "total_seats": 32, "available_seats": 32},
    {"route_id": "R104", "departure_city": "Karachi", "destination_city": "Lahore",
     "departure_time": "07:00 PM", "ticket_price": 5000, "total_seats": 45, "available_seats": 45},
    {"route_id": "R105", "departure_city": "Sukkur", "destination_city": "Hyderabad",
     "departure_time": "02:00 PM", "ticket_price": 1500, "total_seats": 30, "available_seats": 30},
]

# List of dictionaries: bookings (cancelled ones are kept for history)
bookings = []

# Set: every booking ID issued so far (guarantees uniqueness)
issued_booking_ids = set()

# Counter used to build booking IDs such as B1001, B1002, ...
next_booking_number = 1001


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def find_route(route_id):
    """Return the route dictionary for a route ID (case-insensitive), or None."""
    for route in routes:
        if route["route_id"].lower() == route_id.strip().lower():
            return route
    return None


def find_booking(booking_id):
    """Return the booking dictionary for a booking ID (case-insensitive), or None."""
    for booking in bookings:
        if booking["booking_id"].lower() == booking_id.strip().lower():
            return booking
    return None


def seat_status(route):
    """Classify a route as Available, Partially Booked, or Fully Booked."""
    if route["available_seats"] == 0:
        return "Fully Booked"
    elif route["available_seats"] == route["total_seats"]:
        return "Available"
    else:
        return "Partially Booked"


def generate_booking_id():
    """Create a booking ID that is not already in the issued set."""
    global next_booking_number
    new_id = "B" + str(next_booking_number)
    while new_id in issued_booking_ids:
        next_booking_number += 1
        new_id = "B" + str(next_booking_number)
    issued_booking_ids.add(new_id)
    next_booking_number += 1
    return new_id


def read_positive_int(prompt):
    """Read a positive integer. Return None if the input is invalid."""
    text = input(prompt).strip()
    try:
        value = int(text)
    except ValueError:
        return None
    if value <= 0:
        return None
    return value


def print_route_line(route):
    """Print one route in the search-result format."""
    print(f"{route['route_id']} | {route['departure_city']} -> {route['destination_city']} "
          f"| Rs. {route['ticket_price']} | {route['available_seats']} seats available")


# ---------------------------------------------------------------------------
# FEATURE 3: VIEW ROUTES
# ---------------------------------------------------------------------------

def view_routes(only_available=False):
    """List routes. If only_available is True, skip fully booked routes."""
    print("\nAVAILABLE BUS ROUTES")
    print(f"{'No.':<4} {'Route':<6} {'Journey':<28} {'Depart':<9} {'Fare':<9} Seats")
    print("-" * 70)
    shown = 0
    for number, route in enumerate(routes, start=1):
        if only_available and route["available_seats"] == 0:
            continue  # skip fully booked routes when filtering
        journey = f"{route['departure_city']} -> {route['destination_city']}"
        fare = f"Rs.{route['ticket_price']}"
        if route["available_seats"] == 0:
            seats = "Fully Booked"
        else:
            seats = f"{route['available_seats']}/{route['total_seats']}"
        print(f"{number:<4} {route['route_id']:<6} {journey:<28} "
              f"{route['departure_time']:<9} {fare:<9} {seats}")
        shown += 1
    if shown == 0:
        print("No routes to display.")


def view_routes_menu():
    """Sub-menu for option 1: all routes, available only, or schedule."""
    print("\n1. All routes")
    print("2. Only routes with seats available")
    print("3. Schedule grouped by departure city")
    choice = input("Choose a view (press Enter for all routes): ").strip()
    if choice == "2":
        view_routes(only_available=True)
    elif choice == "3":
        view_schedule()
    else:
        view_routes()


# ---------------------------------------------------------------------------
# FEATURE 10: ROUTE SCHEDULE (nested loops)
# ---------------------------------------------------------------------------

def view_schedule():
    print("\nROUTE SCHEDULE BY DEPARTURE CITY")
    for city in SUPPORTED_CITIES:            # outer loop: cities
        print(city)
        found = False
        for route in routes:                 # inner loop: routes
            if route["departure_city"] == city:
                print(f"  {route['route_id']} -> {route['destination_city']} "
                      f"| {route['departure_time']}")
                found = True
        if not found:
            print("  No scheduled departures.")


# ---------------------------------------------------------------------------
# FEATURE 4: SEARCH
# ---------------------------------------------------------------------------

def search_routes():
    term = input("Search by route ID or city: ").strip()
    if term == "":
        print("Please enter a route ID or city name.")
        return
    term_lower = term.lower()
    print()

    # 1) Unique route ID match: stop as soon as it is found.
    for route in routes:
        if route["route_id"].lower() == term_lower:
            print_route_line(route)
            break
    else:
        # 2) No ID match: look for every route touching the city.
        matches = 0
        for route in routes:
            if (route["departure_city"].lower() == term_lower
                    or route["destination_city"].lower() == term_lower):
                print_route_line(route)
                matches += 1
        if matches == 0:
            print(f"No routes found matching '{term}'.")


# ---------------------------------------------------------------------------
# FEATURE 5: BOOK A TICKET
# ---------------------------------------------------------------------------

def book_ticket():
    print("\nBOOK A TICKET")

    # --- Collect and validate everything BEFORE changing any data ---
    name = input("Passenger name: ").strip()
    if name == "":
        print("Error: passenger name cannot be empty. No booking made.")
        return

    age = read_positive_int("Passenger age: ")
    if age is None:
        print("Error: age must be a positive whole number. No booking made.")
        return

    route_id = input("Route ID: ").strip()
    route = find_route(route_id)
    if route is None:
        print(f"Error: route '{route_id}' does not exist. No booking made.")
        return

    seats = read_positive_int("Number of seats: ")
    if seats is None:
        print("Error: seats must be a positive whole number. No booking made.")
        return

    if seats > route["available_seats"]:
        print(f"Error: only {route['available_seats']} seat(s) available on "
              f"{route['route_id']}. No booking made.")
        return

    # --- All checks passed: now create the record and update seats ---
    booking_id = generate_booking_id()
    total_fare = route["ticket_price"] * seats

    booking = {
        "booking_id": booking_id,
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route["route_id"],
        "seats": seats,
        "total_fare": total_fare,
        "status": "Confirmed",
    }
    bookings.append(booking)
    route["available_seats"] -= seats

    print("\nBooking confirmed!")
    print(f"Booking ID: {booking_id}")
    print(f"Passenger: {name}")
    print(f"Route: {route['route_id']} ({route['departure_city']} -> {route['destination_city']})")
    print(f"Seats booked: {seats}")
    print(f"Fare per seat: Rs. {route['ticket_price']}")
    print(f"Total fare: Rs. {total_fare}")
    print("Status: Confirmed")


# ---------------------------------------------------------------------------
# FEATURE 6: VIEW BOOKINGS
# ---------------------------------------------------------------------------

def view_bookings():
    print("\nMY BOOKINGS")
    if len(bookings) == 0:
        print("No bookings found.")
        return
    for number, b in enumerate(bookings, start=1):
        route = find_route(b["route_id"])
        journey = f"{route['departure_city']} -> {route['destination_city']}"
        print(f"{number}. {b['booking_id']} | {b['passenger_name']} (age {b['passenger_age']}) "
              f"| {b['route_id']} {journey} | Seats: {b['seats']} "
              f"| Fare: Rs. {b['total_fare']} | {b['status']}")


# ---------------------------------------------------------------------------
# FEATURE 7: CANCEL A BOOKING
# ---------------------------------------------------------------------------

def cancel_booking():
    booking_id = input("Enter booking ID to cancel: ").strip()
    booking = find_booking(booking_id)

    if booking is None:
        print(f"Booking '{booking_id}' not found. Nothing was changed.")
        return

    if booking["status"] != "Confirmed":
        print(f"Booking {booking['booking_id']} is already cancelled. No seats restored.")
        return

    route = find_route(booking["route_id"])
    # Status change and seat restoration happen together, exactly once.
    booking["status"] = "Cancelled"
    route["available_seats"] += booking["seats"]

    print(f"Booking {booking['booking_id']} has been cancelled.")
    print(f"Seats restored: {booking['seats']}")
    print(f"Route {route['route_id']} available seats: {route['available_seats']}")


# ---------------------------------------------------------------------------
# FEATURE 8: SEAT AVAILABILITY
# ---------------------------------------------------------------------------

def view_seat_availability():
    choice = input("Show only routes with seats remaining? (y/n): ").strip().lower()
    only_available = (choice == "y")

    print("\nSEAT AVAILABILITY")
    shown = 0
    for route in routes:
        if only_available and route["available_seats"] == 0:
            continue
        print(f"{route['route_id']} | {route['departure_city']} -> {route['destination_city']} "
              f"| {route['available_seats']}/{route['total_seats']} seats "
              f"| {seat_status(route)}")
        shown += 1
    if shown == 0:
        print("No routes with seats available.")


# ---------------------------------------------------------------------------
# FEATURE 9: BOOKING REPORT
# ---------------------------------------------------------------------------

def generate_report():
    total_bookings = len(bookings)
    confirmed_count = 0
    cancelled_count = 0
    seats_reserved = 0
    confirmed_revenue = 0
    fully_booked_routes = 0

    for b in bookings:
        if b["status"] == "Confirmed":
            confirmed_count += 1
        else:
            cancelled_count += 1

    # Nested loops: outer visits routes, inner scans matching confirmed bookings
    per_route = []
    for route in routes:
        route_seats = 0
        route_revenue = 0
        for b in bookings:
            if b["route_id"] == route["route_id"] and b["status"] == "Confirmed":
                route_seats += b["seats"]
                route_revenue += b["total_fare"]
        seats_reserved += route_seats
        confirmed_revenue += route_revenue
        if route["available_seats"] == 0:
            fully_booked_routes += 1
        if route_seats > 0:
            per_route.append((route["route_id"], route_seats, route_revenue))

    print("\nBOOKING REPORT")
    print(f"Total bookings created: {total_bookings}")
    print(f"Confirmed bookings: {confirmed_count}")
    print(f"Cancelled bookings: {cancelled_count}")
    print(f"Seats currently reserved: {seats_reserved}")
    print(f"Confirmed revenue: Rs. {confirmed_revenue:,}")
    print(f"Fully booked routes: {fully_booked_routes}")

    if per_route:
        print("\nConfirmed bookings by route:")
        for route_id, seats, revenue in per_route:
            print(f"  {route_id}: {seats} seat(s), Rs. {revenue:,}")


# ---------------------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------------------

def show_menu():
    print("\nSMART BUS RESERVATION SYSTEM")
    print("=" * 32)
    print("1. View Available Routes")
    print("2. Search for a Route")
    print("3. Book a Ticket")
    print("4. View My Bookings")
    print("5. Cancel a Booking")
    print("6. View Seat Availability")
    print("7. Generate Booking Report")
    print("8. Exit")
    print("=" * 32)


def main():
    print("Welcome to the Smart Bus Ticket Booking & Reservation System!")
    while True:
        show_menu()
        try:
            choice_text = input("Enter your choice: ").strip()
        except EOFError:
            break

        if not choice_text.isdigit():
            print("Invalid input. Please enter a number from 1 to 8.")
            continue

        choice = int(choice_text)
        if choice == 1:
            view_routes_menu()
        elif choice == 2:
            search_routes()
        elif choice == 3:
            book_ticket()
        elif choice == 4:
            view_bookings()
        elif choice == 5:
            cancel_booking()
        elif choice == 6:
            view_seat_availability()
        elif choice == 7:
            generate_report()
        elif choice == 8:
            print("Thank you for using Smart Bus. Goodbye!")
            break
        else:
            print("Unsupported choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
