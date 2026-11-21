# Glow & Grace Beauty Parlour — Streamlit site

A simple 4-page site: **Home**, **Services** (with prices and a Book button on each), **Book Now**, and **Staff** (view and cancel bookings, PIN `1234`).

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens at http://localhost:8501

## Files

| File | What it holds |
|---|---|
| `app.py` | The pages (UI only) |
| `services.py` | Parlour name, address, prices, stylists, time slots, images and category colours — edit this to customise |
| `booking.py` | Booking logic + SQLite storage (`bookings.db` is created automatically) |
| `images/` | Placeholder pictures — replace `hero.png`, `hair.jpg`, `skin.jpg`, `makeup.jpg`, `nails.jpg` with real photos (same names) |
| `.streamlit/config.toml` | Colour theme + Poppins font |

## How booking works

- Customer picks services → date → stylist (or "Any available") → free time slot.
- Slots account for the total duration, so a 3-hour bridal booking blocks that stylist for 3 hours.
- Mondays are closed; last appointment must finish by 8 PM. Change these in `services.py` / `booking.py`.

## Adding the booking agent later

All booking logic is in `booking.py`, separate from the UI, so an agent can call the same functions as tools:

```python
from datetime import date
import booking
from services import SERVICES

booking.available_slots(date(2026, 11, 25), ["Hair Spa"], "Any available")
booking.create_booking("Sita", "9876500000", date(2026, 11, 25), "11:00", ["Hair Spa"])
booking.list_bookings(date(2026, 11, 25))
booking.cancel_booking(3)
```

Wrap these as tools for LangChain / an MCP server / a WhatsApp bot, and bookings made by the agent will show up in the Staff page automatically.

Before going live: change `ADMIN_PIN` in `app.py`.
