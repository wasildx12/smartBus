# Smart Bus Ticket Booking & Reservation System

A bus reservation system built two ways:

- **Web app** (`index.html`): a single self-contained page. Browse routes, search, book seats, view and cancel bookings, and see a report. Runs in any browser with no build step.
- **Console app** (`console/main.py`): the original Python 3 version using built-in libraries only.

## Live demo
After enabling GitHub Pages (see below), the site is available at:
`https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`

## Run locally
- Web app: open `index.html` in a browser.
- Console app: `python console/main.py`

## Features
- Five sample routes with seat availability and status
- Search by route ID or city (case-insensitive)
- Booking with validation (name, age, route, seat count, capacity)
- Fare = ticket price × seats, with a unique booking ID per booking
- Cancellation of Confirmed bookings only, restoring seats exactly once
- Booking history that keeps cancelled records
- Report: total, confirmed and cancelled bookings, reserved seats, confirmed revenue (cancelled excluded), fully booked routes
- Route schedule grouped by departure city

## Limitations
Data is stored in memory only. Refreshing the page or closing the program resets everything.

## Structure
```
index.html          Web app
console/main.py     Python console app
console/test_cases.txt
console/README.md   Console app guide
```
