"""Booking logic, kept separate from the UI.

The Streamlit page calls these functions, and your AI booking agent can
call the same ones later as tools:
    available_slots(date, service_names, stylist)
    create_booking(name, phone, date, time, service_names, stylist, notes)
    list_bookings(date=None)
    cancel_booking(booking_id)
"""

import sqlite3
from datetime import date as Date, datetime
from pathlib import Path

from services import CLOSED_WEEKDAYS, STYLISTS, TIME_SLOTS, get_service

DB_PATH = Path(__file__).parent / "bookings.db"
CLOSING_MINUTE = 20 * 60  # 8:00 PM
REAL_STYLISTS = [s for s in STYLISTS if s != "Any available"]


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            services TEXT NOT NULL,
            stylist TEXT NOT NULL,
            total INTEGER NOT NULL,
            notes TEXT,
            status TEXT NOT NULL DEFAULT 'confirmed',
            created_at TEXT NOT NULL
        )"""
    )
    return conn


def _to_min(t: str) -> int:
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def _to_hhmm(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def pretty_time(t: str) -> str:
    """'14:30' -> '2:30 PM'"""
    h, m = map(int, t.split(":"))
    return f"{(h - 1) % 12 + 1}:{m:02d} {'AM' if h < 12 else 'PM'}"


def summarize(service_names: list[str]) -> tuple[int, int]:
    """Return (total price, total minutes) for the chosen services."""
    items = [get_service(n) for n in service_names]
    items = [i for i in items if i]
    return sum(i["price"] for i in items), sum(i["minutes"] for i in items)


def _stylist_free(conn, day: str, stylist: str, start: int, end: int) -> bool:
    rows = conn.execute(
        "SELECT time, end_time FROM bookings WHERE date=? AND stylist=? AND status='confirmed'",
        (day, stylist),
    ).fetchall()
    return all(end <= _to_min(r["time"]) or start >= _to_min(r["end_time"]) for r in rows)


def _free_stylist(conn, day: str, stylist: str, start: int, end: int) -> str | None:
    candidates = REAL_STYLISTS if stylist == "Any available" else [stylist]
    for s in candidates:
        if _stylist_free(conn, day, s, start, end):
            return s
    return None


def is_open(day: Date) -> bool:
    return day.weekday() not in CLOSED_WEEKDAYS


def available_slots(day: Date, service_names: list[str], stylist: str = "Any available") -> list[str]:
    """Start times that still have a free stylist for the whole appointment."""
    if not service_names or not is_open(day) or day < Date.today():
        return []
    _, minutes = summarize(service_names)
    now = datetime.now()
    slots = []
    with _conn() as conn:
        for t in TIME_SLOTS:
            start = _to_min(t)
            end = start + minutes
            if end > CLOSING_MINUTE:
                continue
            if day == Date.today() and start <= now.hour * 60 + now.minute:
                continue
            if _free_stylist(conn, day.isoformat(), stylist, start, end):
                slots.append(t)
    return slots


def create_booking(name, phone, day: Date, time: str, service_names, stylist="Any available", notes=""):
    """Save a booking. Returns the booking as a dict, or raises ValueError."""
    if not name.strip() or not phone.strip():
        raise ValueError("Name and phone are required.")
    if not service_names:
        raise ValueError("Please choose at least one service.")
    total, minutes = summarize(service_names)
    start = _to_min(time)
    end = start + minutes
    with _conn() as conn:
        assigned = _free_stylist(conn, day.isoformat(), stylist, start, end)
        if not assigned or time not in available_slots(day, service_names, stylist):
            raise ValueError("Sorry, that slot was just taken. Please pick another time.")
        cur = conn.execute(
            """INSERT INTO bookings (name, phone, date, time, end_time, services, stylist, total, notes, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (name.strip(), phone.strip(), day.isoformat(), time, _to_hhmm(end),
             ", ".join(service_names), assigned, total, notes.strip(),
             datetime.now().isoformat(timespec="seconds")),
        )
        row = conn.execute("SELECT * FROM bookings WHERE id=?", (cur.lastrowid,)).fetchone()
    return dict(row)


def list_bookings(day: Date | None = None) -> list[dict]:
    with _conn() as conn:
        if day:
            rows = conn.execute("SELECT * FROM bookings WHERE date=? ORDER BY time", (day.isoformat(),))
        else:
            rows = conn.execute("SELECT * FROM bookings ORDER BY date, time")
        return [dict(r) for r in rows.fetchall()]


def cancel_booking(booking_id: int) -> bool:
    with _conn() as conn:
        cur = conn.execute("UPDATE bookings SET status='cancelled' WHERE id=?", (booking_id,))
        return cur.rowcount > 0
