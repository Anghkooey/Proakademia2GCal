from datetime import datetime, timedelta
from ics import Calendar
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from config import calendar_id
from pytz import timezone
from re import search as re_search

COLOR = {
    "Red": "11",
    "Purple": "3",
    "Grey": "8",
    "Green": "10",
    "Blue": "7",
    "Yellow": "5",
}

gc = GoogleCalendar(calendar_id)
tz = timezone(gc.get_settings().timezone)

cutoff = datetime.now() - timedelta(days=30)
for e in gc.get_events(time_min=cutoff):
    gc.delete_event(e.id)

with open("Plany.ics", encoding="utf-8") as f:
    events = Calendar(f.read()).events

for e in events:
    desc = e.description or ""
    if "odwołane" in desc:
        continue

    if "Uwagi: \n" not in desc:
        # Exam
        color_id = COLOR["Red"]
    elif "Sala: \n" in desc:
        # Online or Cancelled
        color_id = COLOR["Purple"]
    elif "Grupy: Wyk" in desc:
        color_id = COLOR["Grey"]
    elif "Grupy: Cw" in desc:
        color_id = COLOR["Green"]
    elif "Grupy: Lab" in desc:
        color_id = COLOR["Blue"]
    else:
        # Unknown event
        color_id = COLOR["Yellow"]

    sala_match = re_search(r"Sala:\s*(?:bud\.)?\s*([A-Z])(?:\s+\1)?\s*(\d+)", desc)
    location = ""
    if sala_match:
        sala_letter, sala_number = sala_match.groups()
        location = f" {sala_letter} {sala_number}"

    summary = f"{location} {e.name}"

    start = tz.localize(e.begin.datetime.replace(tzinfo=None))
    end = tz.localize(e.end.datetime.replace(tzinfo=None))

    gc.add_event(
        Event(summary=summary, start=start, end=end, description=desc, color_id=color_id)
    )
