# Smart Bus Ticket Booking & Reservation System

A text-based Python 3 console application for a small bus service. Users can browse
routes, search, book seats, view bookings, cancel, check seat availability, and
generate reports.

## Requirements
- Python 3.6 or newer
- No external libraries (built-in Python only)

## How to run
```
python main.py
```
(Use `python3 main.py` on macOS/Linux if needed.)

## Menu guide
| Option | Action |
|---|---|
| 1 | View routes. Sub-menu: all routes, only routes with seats, or schedule grouped by departure city |
| 2 | Search by route ID or city (case-insensitive) |
| 3 | Book a ticket: name, age, route ID, number of seats |
| 4 | View all bookings, including cancelled ones |
| 5 | Cancel a Confirmed booking by ID |
| 6 | View seat availability (optional filter for routes with seats left) |
| 7 | Booking report: counts, reserved seats, confirmed revenue, fully booked routes |
| 8 | Exit |

## Sample workflow
1. Choose `3`, enter `Ahmed`, `24`, `R101`, `2`. The booking is confirmed as B1001 for Rs. 2400 and R101 drops to 38/40 seats.
2. Choose `7` to see 1 confirmed booking, 2 seats reserved, Rs. 2,400 revenue.
3. Choose `5`, enter `B1001`. The booking becomes Cancelled and 2 seats are restored.
4. Choose `7` again. Cancelled count is 1 and confirmed revenue is Rs. 0.

## Data structures
- **List of dictionaries** for routes and bookings
- **Tuple** for supported cities
- **Set** for issued booking IDs (guarantees uniqueness)

## Key rules
- All input is validated before any data changes.
- Seats are subtracted only after a valid booking and restored exactly once on cancellation.
- Cancelled bookings stay in history but are excluded from revenue and reserved-seat totals.

## Limitations
All data is stored **in memory only**. Records are lost when the program closes.
There is no database, login, or payment handling.
