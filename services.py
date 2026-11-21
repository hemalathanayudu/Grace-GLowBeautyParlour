"""Parlor details and service menu.

Edit this file to change the name, prices, stylists or pictures.
The booking agent you add later can import SERVICES from here too.
"""

from pathlib import Path

PARLOR = {
    "name": "Glow & Grace Beauty Parlour",
    "tagline": "Hair · Skin · Makeup · Nails",
    "address": "Road No. 12, Banjara Hills, Hyderabad",
    "phone": "+91 98765 43210",
    "hours": "Tue–Sun, 10:00 AM – 8:00 PM (Monday closed)",
    "currency": "₹",
}

# Pictures live in the `images/` folder. To use real salon photos, just
# replace these files with your own (keep the same names), or put a
# full https:// image URL here instead of a file path.
_IMG = Path(__file__).parent / "images"
IMAGES = {
    "hero": str(_IMG / "hero.png"),
    "Hair": str(_IMG / "hair.jpg"),
    "Skin": str(_IMG / "skin.jpg"),
    "Makeup": str(_IMG / "makeup.jpg"),
    "Nails": str(_IMG / "nails.jpg"),
}

STYLISTS = ["Any available", "Priya", "Lakshmi", "Anjali"]

# Each service: name, category, price, duration in minutes, short description
SERVICES = [
    {"name": "Haircut & Styling", "category": "Hair", "price": 499, "minutes": 45, "desc": "Wash, cut and blow-dry styling."},
    {"name": "Hair Spa", "category": "Hair", "price": 999, "minutes": 60, "desc": "Deep-conditioning treatment for soft, shiny hair."},
    {"name": "Global Hair Colour", "category": "Hair", "price": 2499, "minutes": 120, "desc": "Full-head colour with ammonia-free products."},
    {"name": "Keratin Smoothening", "category": "Hair", "price": 4999, "minutes": 180, "desc": "Frizz-free, smooth hair for months."},
    {"name": "Fruit Facial", "category": "Skin", "price": 799, "minutes": 60, "desc": "Refreshing facial for a natural glow."},
    {"name": "Gold Facial", "category": "Skin", "price": 1499, "minutes": 75, "desc": "Brightening facial with gold-infused cream."},
    {"name": "Cleanup", "category": "Skin", "price": 499, "minutes": 30, "desc": "Quick deep-clean for fresh skin."},
    {"name": "Threading (Eyebrows)", "category": "Skin", "price": 60, "minutes": 15, "desc": "Neat eyebrow shaping."},
    {"name": "Full Arms Waxing", "category": "Skin", "price": 399, "minutes": 30, "desc": "Smooth arms with gentle wax."},
    {"name": "Party Makeup", "category": "Makeup", "price": 2499, "minutes": 60, "desc": "Glam look for parties and functions."},
    {"name": "Bridal Makeup", "category": "Makeup", "price": 14999, "minutes": 180, "desc": "Complete bridal look with hairstyle and draping."},
    {"name": "Saree Draping", "category": "Makeup", "price": 499, "minutes": 30, "desc": "Perfect pleats in any style."},
    {"name": "Manicure", "category": "Nails", "price": 599, "minutes": 45, "desc": "Nail shaping, cuticle care and polish."},
    {"name": "Pedicure", "category": "Nails", "price": 799, "minutes": 60, "desc": "Relaxing foot soak, scrub and polish."},
    {"name": "Gel Nail Extensions", "category": "Nails", "price": 1999, "minutes": 90, "desc": "Long-lasting gel nails with a design of your choice."},
]

CATEGORIES = ["Hair", "Skin", "Makeup", "Nails"]

# Colour + emoji per category (used for the colourful cards)
CATEGORY_STYLE = {
    "Hair":   {"emoji": "💇‍♀️", "from": "#FF4E9B", "to": "#B44CFF"},
    "Skin":   {"emoji": "✨", "from": "#FFB03A", "to": "#FF4E6A"},
    "Makeup": {"emoji": "💄", "from": "#FF3CAC", "to": "#6A3CFF"},
    "Nails":  {"emoji": "💅", "from": "#00C2FF", "to": "#7A5CFF"},
}

# Bookable start times (24-hour clock)
TIME_SLOTS = [
    "10:00", "10:30", "11:00", "11:30", "12:00", "12:30",
    "14:00", "14:30", "15:00", "15:30", "16:00", "16:30",
    "17:00", "17:30", "18:00", "18:30", "19:00",
]

CLOSED_WEEKDAYS = [0]  # 0 = Monday


def get_service(name: str) -> dict | None:
    return next((s for s in SERVICES if s["name"] == name), None)
