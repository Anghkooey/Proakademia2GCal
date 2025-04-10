from datetime import datetime, timedelta
from typing import Optional, List
from ics import Calendar as ICSCalendar, Event as ICSEvent
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.calendar import Calendar as GCSACalendar
from pytz import timezone
import re
import os

COLORS = {
    "Lavender": "1",     # Light Purple
    "Sage": "2",         # Light Green
    "Grape": "3",        # Purple
    "Flamingo": "4",     # Coral
    "Banana": "5",       # Yellow
    "Tangerine": "6",    # Orange
    "Peacock": "7",      # Light Blue
    "Graphite": "8",     # Grey
    "Blueberry": "9",    # Blue
    "Basil": "10",       # Green
    "Tomato": "11",      # Red
}

KEEP_PATTERN = re.compile(r"^(Sala|Uwagi|Prowadzący):\s*\S+")


def determine_color(desc: str) -> str:
    if "Uwagi: \n" not in desc:
        return COLORS["Tomato"]  # Exam
    elif "Sala: \n" in desc:
        return COLORS["Grape"]  # Online or cancelled
    elif "Grupy: Wyk" in desc:
        return COLORS["Graphite"]
    elif any(k in desc for k in ["Grupy: Cw", "Grupy: Lek"]):
        return COLORS["Basil"]
    elif "Grupy: Lab" in desc:
        return COLORS["Peacock"]
    return COLORS["Banana"]  # Default


def extract_location(desc: str) -> str:
    match = re.search(r"Sala:\s*(?:bud\.)?\s*([A-Z])(?:\s+\1)?\s*(\d+)", desc)
    return f"{match.group(1)} {match.group(2)}" if match else ""


def clean_description(desc: str) -> str:
    return "\n".join(
        line for line in desc.splitlines() if KEEP_PATTERN.match(line.strip())
    ).strip()


def load_ics_events(path: str) -> List:
    with open(path, encoding="utf-8") as f:
        return list(ICSCalendar(f.read()).events)


def ics_import(calendar_id: Optional[str] = None, ics_path: str = "Plany.ics", open_browser: bool = True):
    gc = GoogleCalendar(open_browser=open_browser)

    if calendar_id:
        if gc.get_calendar().id == gc.get_calendar(calendar_id).id:
            confirmation = input(
                "You are about to use your primary calendar. All existing events will be deleted. Proceed? (yes/no): "
            )
            if confirmation.lower() != 'yes':
                print("Operation aborted.")
                exit()
        gc = GoogleCalendar(calendar_id)
    else:
        for calendar in gc.get_calendar_list():
            if calendar.summary == "Study":
                gc.delete_calendar(calendar.id)
                print(f"Deleted old calendar: {calendar.id}")

        calendar_id = gc.add_calendar(GCSACalendar("Study")).calendar_id
        gc = GoogleCalendar(calendar_id, open_browser=open_browser)
        print(f"Created new calendar: {calendar_id}")

    tz = timezone(gc.get_settings().timezone)
    cutoff = datetime.now() - timedelta(days=30)

    for e in gc.get_events(time_min=cutoff):
        gc.delete_event(e.id)

    for e in load_ics_events(ics_path):
        desc = e.description or ""
        if "odwołane" in desc:
            continue

        location = extract_location(desc)
        summary = f"{location} {e.name}".strip()
        cleaned_desc = clean_description(desc)

        start = tz.localize(e.begin.datetime.replace(tzinfo=None))
        end = tz.localize(e.end.datetime.replace(tzinfo=None))

        gc.add_event(Event(summary=summary, start=start, end=end, description=cleaned_desc, color_id=determine_color(desc)))


def ics_edit(input_path: str = "Plany.ics", output_path: str = "Plany_edited.ics", timezone_str: str = "Europe/Warsaw"):
    events = load_ics_events(input_path)
    new_cal = ICSCalendar()
    tz = timezone(timezone_str)

    for e in events:
        if "odwołane" in (e.description or ""): continue
        location = extract_location(e.description)
        new_summary = f"{location} {e.name}".strip()
        cleaned_desc = clean_description(e.description)

        # Localize start and end times to the specified timezone
        start = tz.localize(e.begin.datetime.replace(tzinfo=None))
        end = tz.localize(e.end.datetime.replace(tzinfo=None))

        # Add event to new calendar
        new_event = ICSEvent(
            name=new_summary,
            begin=start,
            end=end,
            description=cleaned_desc,
            location=location or None
        )
        new_cal.events.add(new_event)

    # Ensure the directory exists for the output file
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Write the updated calendar to the output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(new_cal.serialize_iter())

