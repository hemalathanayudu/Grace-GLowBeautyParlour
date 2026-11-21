"""Beauty parlour website in Streamlit — colourful, modern version.

Run with:  streamlit run app.py
"""

import base64
import json
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components

import booking
from services import CATEGORIES, CATEGORY_STYLE, IMAGES, PARLOR, SERVICES, STYLISTS

st.set_page_config(page_title=PARLOR["name"], page_icon="💅", layout="wide")

ADMIN_PIN = "1234"  # change this before going live
CUR = PARLOR["currency"]
MAIN_GRADIENT = "linear-gradient(120deg,#FF3CAC 0%,#C14BFF 50%,#5B6CFF 100%)"

# n8n chat agent (Chat Trigger node → Mode: Embedded Chat, Public: on, Allowed Origins: *)
N8N_CHAT_URL = "https://superaiagentic.app.n8n.cloud/webhook/c651a451-422e-446b-9f8a-aa46c0678f0a/chat"


# ---------------- Helpers ----------------

def html(markup: str):
    """Render HTML (joined to one line so Markdown never turns it into code)."""
    st.markdown(" ".join(line.strip() for line in markup.splitlines()), unsafe_allow_html=True)


@st.cache_data
def img_src(path_or_url: str) -> str:
    """Local images are embedded so they work inside HTML cards."""
    if path_or_url.startswith("http"):
        return path_or_url
    p = Path(path_or_url)
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


def money(n: int) -> str:
    return f"{CUR}{n:,}"


def grad(cat: str) -> str:
    s = CATEGORY_STYLE[cat]
    return f"linear-gradient(135deg,{s['from']},{s['to']})"


def page_head(title: str, sub: str):
    html(f"<div class='page-head'><h1>{title}</h1><p>{sub}</p></div>")


def service_card(s: dict) -> str:
    style = CATEGORY_STYLE[s["category"]]
    return f"""
    <div class='svc' style='--g:{grad(s["category"])}'>
      <div class='top'><span class='chip'>{style['emoji']} {s['category']}</span>
      <span class='dur'>⏱ {s['minutes']} min</span></div>
      <div class='title'>{s['name']}</div>
      <div class='desc'>{s['desc']}</div>
      <div class='bottom'><span class='price'>{money(s['price'])}</span>
      <a class='book-link' href='book?service={quote(s["name"])}' target='_self'>Book →</a></div>
    </div>"""


def show_chat_agent(height: int = 620):
    """n8n chat agent, styled to match the site colours."""
    welcome = json.dumps([
        f"Hi! Welcome to {PARLOR['name']} 💖",
        "Ask me about services, prices, timings or booking.",
    ], ensure_ascii=False)
    title = json.dumps(f"{PARLOR['name']} Assistant", ensure_ascii=False)

    components.html(f"""
    <link href="https://cdn.jsdelivr.net/npm/@n8n/chat/dist/style.css" rel="stylesheet" />
    <style>
      html, body {{ margin:0; padding:6px; height:100%; box-sizing:border-box; background:transparent; }}
      #n8n-chat {{ height:{height - 24}px; border-radius:26px; overflow:hidden;
                  box-shadow:0 14px 36px rgba(193,75,255,.22); }}
      :root {{
        --chat--color-primary: #FF3CAC;
        --chat--color-primary-shade-50: #E5358F;
        --chat--color-primary-shade-100: #C2187A;
        --chat--color-secondary: #7A5CFF;
        --chat--color-secondary-shade-50: #6A3CFF;
        --chat--header--background: linear-gradient(120deg,#FF3CAC,#C14BFF,#5B6CFF);
        --chat--header--color: #ffffff;
        --chat--message--user--background: #7A5CFF;
        --chat--message--user--color: #ffffff;
        --chat--border-radius: 18px;
      }}
    </style>
    <div id="n8n-chat"></div>
    <script type="module">
      import {{ createChat }} from 'https://cdn.jsdelivr.net/npm/@n8n/chat/dist/chat.bundle.es.js';
      createChat({{
        webhookUrl: '{N8N_CHAT_URL}',
        target: '#n8n-chat',
        mode: 'fullscreen',
        showWelcomeScreen: false,
        initialMessages: {welcome},
        i18n: {{
          en: {{
            title: {title},
            subtitle: 'Ask us anything, we reply instantly',
            footer: '',
            getStarted: 'New Conversation',
            inputPlaceholder: 'Type your question...',
          }},
        }},
      }});
    </script>
    """, height=height)


# ---------------- Styles ----------------

html(f"""
<style>
#MainMenu, [data-testid="stAppDeployButton"], [data-testid="stToolbarActions"] {{display:none !important;}}
.block-container {{max-width: 1150px; padding-top: 4.5rem; padding-bottom: 1rem;}}
.stApp {{background:
  radial-gradient(circle at 8% 0%, #FFE0F0 0, transparent 32%),
  radial-gradient(circle at 96% 8%, #E6DEFF 0, transparent 34%),
  radial-gradient(circle at 70% 100%, #FFEBD6 0, transparent 40%), #FFF7FB;}}
a {{text-decoration: none !important;}}

.hero {{background:{MAIN_GRADIENT}; border-radius: 34px; padding: 44px 48px; display:flex; align-items:center;
  gap: 20px; color:#fff; box-shadow: 0 24px 60px rgba(193,75,255,.35); overflow:hidden;}}
.hero .txt {{flex: 1.25;}}
.hero img {{width: 40%; max-width: 420px;}}
.badge {{display:inline-block; background:rgba(255,255,255,.22); padding:7px 16px; border-radius:999px; font-size:.85rem; font-weight:600;}}
.hero h1 {{color:#fff; font-size: 3.3rem; line-height:1.05; margin: 16px 0 12px; font-weight:800; padding:0;}}
.hero p {{color: rgba(255,255,255,.93); font-size:1.08rem; margin-bottom: 8px;}}
.btn {{display:inline-block; padding: 13px 28px; border-radius:999px; font-weight:700; margin: 10px 10px 0 0; transition: transform .15s;}}
.btn:hover {{transform: translateY(-2px);}}
.btn-white {{background:#fff; color:#C2187A !important; box-shadow: 0 10px 24px rgba(0,0,0,.15);}}
.btn-ghost {{border:2px solid rgba(255,255,255,.85); color:#fff !important;}}
.stats {{display:flex; gap:12px; margin-top: 26px; flex-wrap: wrap;}}
.stat {{background: rgba(255,255,255,.18); border-radius: 18px; padding: 10px 18px; font-size:.85rem;}}
.stat b {{font-size: 1.35rem; display:block;}}

.section-title {{font-size: 2rem; font-weight: 800; margin: 46px 0 4px;}}
.section-sub {{color:#8A7790; margin-bottom: 18px;}}
.grad-text {{background: linear-gradient(90deg,#FF3CAC,#7A5CFF); -webkit-background-clip:text; background-clip:text; color: transparent;}}

.cat-grid {{display:grid; grid-template-columns: repeat(4,1fr); gap:18px;}}
.cat-card {{border-radius: 26px; overflow:hidden; display:block; transition: transform .2s; box-shadow: 0 14px 32px rgba(122,92,255,.18);}}
.cat-card:hover {{transform: translateY(-6px) rotate(-.5deg);}}
.cat-card img {{width:100%; display:block; aspect-ratio: 4/3; object-fit: cover;}}
.cat-card .body {{padding: 14px 18px 18px;}}
.cat-card .name {{font-weight: 800; font-size: 1.2rem; color:#fff;}}
.cat-card .from {{color:#fff; opacity:.92; font-size:.9rem;}}

.svc-grid {{display:grid; grid-template-columns: repeat(3,1fr); gap:18px;}}
.svc {{background:#fff; border-radius: 24px; padding: 22px 20px 18px; box-shadow: 0 10px 30px rgba(122,92,255,.10);
  border: 1px solid #F6E4F0; display:flex; flex-direction:column; gap:8px; position:relative; overflow:hidden; transition: transform .2s;}}
.svc:hover {{transform: translateY(-4px);}}
.svc::before {{content:""; position:absolute; left:0; right:0; top:0; height:7px; background: var(--g);}}
.svc .top {{display:flex; justify-content: space-between; align-items:center;}}
.chip {{font-size:.78rem; font-weight:600; padding:4px 11px; border-radius:999px; background:#F5EEFF; color:#6A3CFF;}}
.dur {{font-size:.8rem; color:#9A8AA0;}}
.svc .title {{font-weight:700; font-size:1.08rem;}}
.svc .desc {{color:#7A6680; font-size:.9rem; flex:1;}}
.svc .bottom {{display:flex; justify-content:space-between; align-items:center; margin-top:6px;}}
.price {{font-weight:800; font-size:1.35rem; background: var(--g); -webkit-background-clip:text; background-clip:text; color:transparent;}}
.book-link {{background: var(--g); color:#fff !important; padding:8px 18px; border-radius:999px; font-weight:700; font-size:.9rem;}}

.why {{display:grid; grid-template-columns: repeat(3,1fr); gap:18px;}}
.why > div {{background:#fff; border-radius:24px; padding:22px; border:1px solid #F6E4F0;}}
.why .ic {{font-size: 1.6rem; width:52px; height:52px; border-radius:16px; display:flex; align-items:center; justify-content:center; margin-bottom:10px;}}
.why b {{font-size:1.05rem;}}
.why p {{color:#7A6680; font-size:.9rem; margin:4px 0 0;}}

.cta {{margin-top:44px; border-radius:30px; padding: 30px 40px; background: linear-gradient(120deg,#FFB03A,#FF4E6A 50%,#FF3CAC);
  color:#fff; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;}}
.cta h3 {{color:#fff; margin:0; font-size:1.7rem; padding:0;}}
.cta p {{margin:4px 0 0; opacity:.92;}}
.footer {{text-align:center; color:#9A8AA0; font-size:.85rem; margin-top:40px; padding: 18px 0;}}

.page-head {{border-radius: 28px; padding: 30px 36px; color:#fff; background:{MAIN_GRADIENT}; margin-bottom: 22px;
  box-shadow: 0 18px 44px rgba(193,75,255,.28);}}
.page-head h1 {{color:#fff; margin:0; padding:0; font-size: 2.4rem;}}
.page-head p {{color: rgba(255,255,255,.92); margin: 4px 0 0;}}

.step {{display:flex; align-items:center; gap:10px; font-weight:700; font-size:1.08rem; margin: 20px 0 6px;}}
.step span {{display:inline-flex; width:30px; height:30px; border-radius:50%; align-items:center; justify-content:center;
  color:#fff; background: linear-gradient(135deg,#FF3CAC,#7A5CFF); font-size:.9rem;}}
.summary {{background:#fff; border-radius:26px; padding:24px; border: 1px solid #F6E4F0; box-shadow: 0 14px 36px rgba(229,53,143,.14); margin-top: 20px;}}
.summary h4 {{margin:0 0 10px; padding:0;}}
.summary .row {{display:flex; justify-content:space-between; padding: 7px 0; border-bottom: 1px dashed #F0DDEA; font-size:.93rem;}}
.summary .total {{display:flex; justify-content:space-between; align-items:center; margin-top: 12px;}}
.summary .total b {{font-size:1.9rem; font-weight:800;}}
.summary .muted {{color:#9A8AA0; font-size:.9rem;}}
.done {{border-radius:28px; padding: 34px; text-align:center; color:#fff; background: linear-gradient(120deg,#2BD9A0,#00C2FF 55%,#7A5CFF); margin-bottom: 18px;}}
.done h2 {{color:#fff; margin: 6px 0; padding:0;}}
.done .big {{font-size: 3rem;}}

.metrics {{display:grid; grid-template-columns: repeat(3,1fr); gap:16px; margin-bottom: 18px;}}
.metric {{border-radius:22px; padding:20px 22px; color:#fff;}}
.metric b {{font-size:2rem; display:block;}}

.chat-tips {{display:flex; flex-direction:column; gap:12px;}}
.chat-tips > div {{background:#fff; border-radius:20px; padding:16px 18px; border:1px solid #F6E4F0;
  box-shadow: 0 8px 22px rgba(122,92,255,.08); font-size:.93rem; color:#5E4B66;}}
.chat-tips b {{display:block; color:#2B1B33; margin-bottom:2px;}}

.stButton button[kind="primary"] {{background: linear-gradient(120deg,#FF3CAC,#7A5CFF) !important; border:none !important;
  color:#fff !important; font-weight:700; padding: .7rem 1.6rem; box-shadow: 0 10px 22px rgba(229,53,143,.35);}}

@media (max-width: 820px) {{
  .hero {{flex-direction:column; padding:28px;}} .hero img {{width:70%;}} .hero h1 {{font-size:2.3rem;}}
  .cat-grid {{grid-template-columns:repeat(2,1fr);}} .svc-grid, .why, .metrics {{grid-template-columns:1fr;}}
}}
</style>
""")


# ---------------- Pages ----------------

def home():
    html(f"""
    <div class='hero'>
      <div class='txt'>
        <span class='badge'>✨ {PARLOR['name']}</span>
        <h1>Look good.<br>Feel amazing.</h1>
        <p>Hair, skin, makeup and nails by friendly experts. Book your slot in under a minute.</p>
        <a class='btn btn-white' href='book' target='_self'>📅 Book now</a>
        <a class='btn btn-ghost' href='chat' target='_self'>💬 Ask us</a>
        <div class='stats'>
          <div class='stat'><b>{len(SERVICES)}+</b>services</div>
          <div class='stat'><b>{len(STYLISTS) - 1}</b>expert stylists</div>
          <div class='stat'><b>6 days</b>a week</div>
        </div>
      </div>
      <img src='{img_src(IMAGES["hero"])}' alt=''>
    </div>""")

    html("<div class='section-title'>What would you like <span class='grad-text'>today?</span></div>"
         "<div class='section-sub'>Pick a category to see all services and prices.</div>")
    cards = ""
    for cat in CATEGORIES:
        start = min(s["price"] for s in SERVICES if s["category"] == cat)
        cards += f"""
        <a class='cat-card' href='services?cat={cat}' target='_self' style='background:{grad(cat)}'>
          <img src='{img_src(IMAGES[cat])}' alt='{cat}'>
          <div class='body'><div class='name'>{CATEGORY_STYLE[cat]['emoji']} {cat}</div>
          <div class='from'>from {money(start)}</div></div>
        </a>"""
    html(f"<div class='cat-grid'>{cards}</div>")

    html("<div class='section-title'>Most <span class='grad-text'>loved</span></div>"
         "<div class='section-sub'>Our customers' favourite treatments.</div>")
    popular = ["Hair Spa", "Gold Facial", "Party Makeup"]
    html("<div class='svc-grid'>" + "".join(service_card(s) for s in SERVICES if s["name"] in popular) + "</div>")

    html("""
    <div class='section-title'>Why <span class='grad-text'>choose us</span></div><div class='section-sub'>&nbsp;</div>
    <div class='why'>
      <div><div class='ic' style='background:#FFE3F1'>🧴</div><b>Quality products</b><p>Trusted brands, gentle on skin and hair.</p></div>
      <div><div class='ic' style='background:#E9E3FF'>👩‍🎨</div><b>Trained experts</b><p>Friendly stylists who listen to what you want.</p></div>
      <div><div class='ic' style='background:#FFF0D9'>🧼</div><b>Clean & hygienic</b><p>Sanitised tools and fresh towels, every time.</p></div>
    </div>""")

    # ---- Chat agent on the Home page ----
    html("<div class='section-title'>Have a <span class='grad-text'>question?</span></div>"
         "<div class='section-sub'>Chat with our assistant — it replies instantly, any time.</div>")
    show_chat_agent(height=540)

    html(f"""
    <div class='cta'>
      <div><h3>Ready for your glow-up? 💖</h3><p>📍 {PARLOR['address']} · 📞 {PARLOR['phone']} · 🕒 {PARLOR['hours']}</p></div>
      <a class='btn btn-white' href='book' target='_self'>Book appointment →</a>
    </div>""")


def services_page():
    page_head("Services & Prices 💅", "Transparent prices. No surprises. Tap Book on anything you like.")
    options = ["All"] + CATEGORIES
    start = st.query_params.get("cat", "All")
    pick = st.pills("Category", options, default=start if start in options else "All",
                    format_func=lambda c: c if c == "All" else f"{CATEGORY_STYLE[c]['emoji']} {c}",
                    label_visibility="collapsed")
    pick = pick or "All"
    shown = [s for s in SERVICES if pick == "All" or s["category"] == pick]
    html("<div class='svc-grid'>" + "".join(service_card(s) for s in shown) + "</div>")


def book():
    # Arriving from a "Book" button carries the service in the link
    svc = st.query_params.get("service")
    if svc:
        if any(s["name"] == svc for s in SERVICES):
            st.session_state["chosen_services"] = [svc]
        st.query_params.clear()

    if "last_booking" in st.session_state:
        b = st.session_state.pop("last_booking")
        html(f"""
        <div class='done'><div class='big'>🎉</div><h2>You're booked, {b['name']}!</h2>
        <p>{b['services']}<br><b>{date.fromisoformat(b['date']).strftime('%a, %d %b %Y')} at {booking.pretty_time(b['time'])}</b>
        with {b['stylist']} · Booking #{b['id']} · {money(b['total'])}</p></div>""")
        if st.button("Book another", type="primary"):
            st.rerun()
        return

    page_head("Book an Appointment 📅", "Four quick steps and you're done.")
    left, right = st.columns([1.6, 1], gap="large")

    with left:
        html("<div class='step'><span>1</span>Choose your services</div>")
        chosen = st.multiselect("Services", [s["name"] for s in SERVICES], key="chosen_services",
                                placeholder="Tap to choose one or more", label_visibility="collapsed")

        html("<div class='step'><span>2</span>Pick a date & stylist</div>")
        c1, c2 = st.columns(2)
        day = c1.date_input("Date", min_value=date.today(), max_value=date.today() + timedelta(days=60),
                            format="DD/MM/YYYY")
        stylist = c2.selectbox("Stylist", STYLISTS)

        html("<div class='step'><span>3</span>Pick a time</div>")
        time = None
        if not chosen:
            st.caption("Choose a service first to see free times.")
        elif not booking.is_open(day):
            st.warning("We're closed on Mondays — please pick another day.")
        else:
            slots = booking.available_slots(day, chosen, stylist)
            if slots:
                time = st.pills("Time", slots, key=f"time_{day}_{stylist}_{'|'.join(chosen)}",
                                format_func=booking.pretty_time, label_visibility="collapsed")
            else:
                st.warning("No free times that day. Try another date or stylist.")

        html("<div class='step'><span>4</span>Your details</div>")
        n1, n2 = st.columns(2)
        name = n1.text_input("Your name", placeholder="e.g. Priya")
        phone = n2.text_input("Phone number", placeholder="10-digit mobile")
        notes = st.text_area("Anything we should know? (optional)", height=80)

        if st.button("Confirm booking ✨", type="primary", width="stretch"):
            if not chosen:
                st.error("Please choose at least one service.")
            elif not time:
                st.error("Please pick a time.")
            elif not name.strip() or not phone.strip():
                st.error("Please enter your name and phone number.")
            else:
                try:
                    st.session_state["last_booking"] = booking.create_booking(
                        name, phone, day, time, chosen, stylist, notes)
                    del st.session_state["chosen_services"]
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

    with right:
        total, minutes = booking.summarize(chosen)
        rows = "".join(
            f"<div class='row'><span>{s['name']}</span><span>{money(s['price'])}</span></div>"
            for s in SERVICES if s["name"] in chosen
        ) or "<p class='muted'>No services chosen yet.</p>"
        when = day.strftime("%a, %d %b")
        if time:
            when += f" · {booking.pretty_time(time)}"
        html(f"""
        <div class='summary'>
          <h4>Your booking</h4>{rows}
          <div class='row'><span>📅 When</span><span>{when}</span></div>
          <div class='row'><span>💇‍♀️ Stylist</span><span>{stylist}</span></div>
          <div class='row'><span>⏱ Duration</span><span>{minutes} min</span></div>
          <div class='total'><span class='muted'>Total</span><b class='grad-text'>{money(total)}</b></div>
        </div>""")


def chat_page():
    page_head("Ask Us 💬", "Questions about services, prices or timings? Our assistant replies instantly.")
    left, right = st.columns([1.7, 1], gap="large")
    with left:
        show_chat_agent(height=640)
    with right:
        html(f"""
        <div class='chat-tips'>
          <div><b>💅 Try asking</b>"How much is a hair spa?"<br>"Do you do bridal makeup?"<br>"Are you open on Sunday?"</div>
          <div><b>🕒 Timings</b>{PARLOR['hours']}</div>
          <div><b>📍 Visit us</b>{PARLOR['address']}</div>
          <div><b>📞 Call us</b>{PARLOR['phone']}</div>
        </div>""")
        st.page_link(book_page, label="Book an appointment", icon="📅")


def admin():
    page_head("Staff Dashboard 🔒", "See and manage all bookings.")
    if not st.session_state.get("is_admin"):
        c, _ = st.columns([1, 2])
        pin = c.text_input("Staff PIN", type="password")
        if c.button("Unlock", type="primary"):
            if pin == ADMIN_PIN:
                st.session_state["is_admin"] = True
                st.rerun()
            else:
                st.error("Wrong PIN.")
        return

    all_rows = booking.list_bookings()
    today = date.today().isoformat()
    todays = [r for r in all_rows if r["date"] == today and r["status"] == "confirmed"]
    upcoming = [r for r in all_rows if r["date"] >= today and r["status"] == "confirmed"]
    html(f"""
    <div class='metrics'>
      <div class='metric' style='background:linear-gradient(135deg,#FF4E9B,#B44CFF)'><b>{len(todays)}</b>bookings today</div>
      <div class='metric' style='background:linear-gradient(135deg,#FFB03A,#FF4E6A)'><b>{money(sum(r['total'] for r in todays))}</b>today's revenue</div>
      <div class='metric' style='background:linear-gradient(135deg,#00C2FF,#7A5CFF)'><b>{len(upcoming)}</b>upcoming bookings</div>
    </div>""")

    show_all = st.toggle("Show all dates", value=True)
    day = None if show_all else st.date_input("Date", value=date.today(), format="DD/MM/YYYY")
    rows = booking.list_bookings(day)
    if not rows:
        st.info("No bookings yet.")
        return
    st.dataframe(rows, width="stretch", hide_index=True,
                 column_order=["id", "date", "time", "end_time", "name", "phone",
                               "services", "stylist", "total", "status", "notes"])
    confirmed = [r for r in rows if r["status"] == "confirmed"]
    if confirmed:
        c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
        pick = c1.selectbox("Cancel a booking", confirmed, index=None,
                            format_func=lambda r: f"#{r['id']} · {r['date']} {r['time']} · {r['name']}")
        if c2.button("Cancel booking", disabled=pick is None, width="stretch"):
            booking.cancel_booking(pick["id"])
            st.rerun()


# ---------------- Navigation ----------------

book_page = st.Page(book, title="Book Now", icon="📅", url_path="book")

nav = st.navigation([
    st.Page(home, title="Home", icon="🏠", default=True),
    st.Page(services_page, title="Services", icon="💅", url_path="services"),
    book_page,
    st.Page(chat_page, title="Ask Us", icon="💬", url_path="chat"),
    st.Page(admin, title="Staff", icon="🔒", url_path="staff"),
], position="top")
nav.run()

html(f"<div class='footer'>💖 {PARLOR['name']} · {PARLOR['phone']} · {PARLOR['address']}</div>")