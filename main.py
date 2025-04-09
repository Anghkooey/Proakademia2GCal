from datetime import datetime, timedelta
from random import randint
from ics import Calendar as ICSCalendar
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.calendar import Calendar as GCSACalendar
from pytz import timezone
import re

def import_ics(calendar_id: str = None, ics_path: str = "Plany.ics", open_browser: bool = True):
    COLOR = {
        "Red": "11",
        "Purple": "3",
        "Grey": "8",
        "Green": "10",
        "Blue": "7",
        "Yellow": "5",
    }

    keep_pattern = re.compile(r"^(Sala|Uwagi|Prowadzący):\s*\S+")
    
    # Create or get Google Calendar
    if calendar_id:
        gc = GoogleCalendar(calendar_id)
    else:
        calendar_name = f"Study_{datetime.now():%d%m%Y}_{randint(0, 1000)}"
        gc = GoogleCalendar(open_browser=open_browser)
        calendar_id = gc.add_calendar(GCSACalendar(calendar_name)).calendar_id
        print(f"Created new calendar: {calendar_name}\nCalendar ID: {calendar_id}")

    # Set timezone based on the calendar settings
    tz = timezone(gc.get_settings().timezone)

    # Clean up old events from the last 30 days
    cutoff = datetime.now() - timedelta(days=30)
    for e in gc.get_events(time_min=cutoff):
        gc.delete_event(e.id)

    # Read events from the ICS file
    with open(ics_path, encoding="utf-8") as f:
        events = ICSCalendar(f.read()).events

    # Process each event
    for e in events:
        desc = e.description or ""
        if "odwołane" in desc:
            continue

        # Determine color based on description content
        if "Uwagi: \n" not in desc:
            color_id = COLOR["Red"]
        elif "Sala: \n" in desc:
            color_id = COLOR["Purple"]
        elif "Grupy: Wyk" in desc:
            color_id = COLOR["Grey"]
        elif any(k in desc for k in ["Grupy: Cw", "Grupy: Lek"]):
            color_id = COLOR["Green"]
        elif "Grupy: Lab" in desc:
            color_id = COLOR["Blue"]
        else:
            color_id = COLOR["Yellow"]

        # Extract location (Sala)
        sala_match = re.search(r"Sala:\s*(?:bud\.)?\s*([A-Z])(?:\s+\1)?\s*(\d+)", desc)
        location = f"{sala_match.group(1)} {sala_match.group(2)}" if sala_match else ""

        summary = f"{location} {e.name}"

        # Set event start and end time in the correct timezone
        start = tz.localize(e.begin.datetime.replace(tzinfo=None))
        end = tz.localize(e.end.datetime.replace(tzinfo=None))

        # Clean up description, keeping only relevant lines
        desc_lines = desc.splitlines()
        cleaned_desc = "\n".join(
            line for line in desc_lines if keep_pattern.match(line.strip())
        ).strip()

        # Add the event to Google Calendar
        gc.add_event(
            Event(summary=summary, start=start, end=end, description=cleaned_desc, color_id=color_id)
        )
