from datetime import datetime, timedelta
from typing import Optional, List
from ics import Calendar as ICSCalendar, Event as ICSEvent
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.calendar import Calendar as GCSACalendar
from pytz import timezone
import re
import os

# Color mapping for calendar events based on descriptions
COLORS = {
    "Lavender": "1",  # Light Purple
    "Sage": "2",  # Light Green
    "Grape": "3",  # Purple
    "Flamingo": "4",  # Coral
    "Banana": "5",  # Yellow
    "Tangerine": "6",  # Orange
    "Peacock": "7",  # Light Blue
    "Graphite": "8",  # Grey
    "Blueberry": "9",  # Blue
    "Basil": "10",  # Green
    "Tomato": "11",  # Red
}

# Regex pattern to extract certain lines from descriptions (Sala, Uwagi, Prowadzący)
KEEP_PATTERN = re.compile(r"^(Sala|Uwagi|Prowadzący|Grupy):\s*\S+")


def determine_color(desc: str) -> str:
    """
    Determines the color ID for the event based on the content of the description.

    Parameters:
    - desc (str): The description text of the event.

    Returns:
    - str: Color ID corresponding to the event type.

    Algorithm:
    1. Exam events (without "Uwagi") are assigned a red color.
    2. Online/cancelled events (with "Sala") are assigned a purple color.
    3. Events with specific group types (e.g., "Wyk", "Cw", "Lek", "Lab") are assigned corresponding colors.
    4. Default color is yellow if no specific type is detected.
    """
    if not any(k in desc for k in ("Uwagi: \n", "Uwagi:  obieralny")):
        return COLORS["Tomato"]  # Exam
    elif "Sala: \n" in desc:
        return COLORS["Grape"]  # Online or cancelled
    elif "Grupy: Wyk" in desc:
        return COLORS["Graphite"]
    elif any(k in desc for k in ("Grupy: Cw", "Grupy: Lek")):
        return COLORS["Basil"]
    elif "Grupy: Lab" in desc:
        return COLORS["Peacock"]
    return COLORS["Banana"]  # Default


def extract_location(desc: str) -> str:
    """
    Extracts the location (Sala) information from the event description.

    Parameters:
    - desc (str): The description text of the event.

    Returns:
    - str: Extracted location (if any), otherwise an empty string.

    Algorithm:
    1. Uses regex to match the "Sala" and room number in the description.
    2. Returns the formatted location string (e.g., "A 101").
    """
    match = re.search(r"Sala:\s*(?:bud\.)?\s*([A-Z])(?:\s+\1)?\s*(\d+)", desc)
    return f"{match.group(1)} {match.group(2)}" if match else ""


def clean_description(desc: str) -> str:
    """
    Cleans the event description by keeping only relevant lines (Sala, Uwagi, Prowadzący).

    Parameters:
    - desc (str): The description text of the event.

    Returns:
    - str: Cleaned description containing only relevant lines.

    Algorithm:
    1. Splits the description into lines.
    2. Filters lines matching the KEEP_PATTERN regex.
    3. Returns a cleaned description with the relevant lines joined together.
    """
    return "\n".join(
        line for line in desc.splitlines() if KEEP_PATTERN.match(line.strip())
    ).strip()


def load_ics_events(path: str) -> List:
    """
    Loads events from an ICS file.

    Parameters:
    - path (str): The path to the ICS file.

    Returns:
    - List: List of events parsed from the ICS file.

    Algorithm:
    1. Opens the ICS file and parses its content.
    2. Extracts and returns all events from the ICS calendar.
    """
    with open(path, encoding="utf-8") as f:
        return list(ICSCalendar(f.read()).events)


def ics_import(
    calendar_id: Optional[str] = None,
    ics_path: str = "Plany.ics",
    open_browser: bool = True,
):
    """
    Imports events from an ICS file into a Google Calendar, either creating a new calendar or updating an existing one.

    Parameters:
    - calendar_id (Optional[str]): The ID of an existing Google Calendar to import events into. If None, creates a new calendar.
    - ics_path (str): Path to the ICS file containing the events to import.
    - open_browser (bool): Flag indicating whether to open a browser for Google authentication.

    Algorithm:
    1. If a calendar ID is provided, uses that calendar.
    2. If no calendar ID is provided, checks for an existing 'Study' calendar and deletes it.
    3. Creates a new calendar if necessary, or reuses the existing one.
    4. Fetches events from the last 30 days and deletes them.
    5. Loads events from the ICS file.
    6. Determines the color for each event, extracts the location, and cleans the description.
    7. Adds each event to the Google Calendar with the appropriate time zone and other details.
    """
    gc = GoogleCalendar(open_browser=open_browser)

    if calendar_id:
        if gc.get_calendar().id == gc.get_calendar(calendar_id).id:
            confirmation = input(
                "You are about to use your primary calendar. All existing events will be deleted. Proceed? (yes/no): "
            )
            if confirmation.lower() != "yes":
                print("Operation aborted.")
                exit()
        gc = GoogleCalendar(calendar_id)
        cutoff = datetime.now() - timedelta(days=30)

        for e in gc.get_events(time_min=cutoff):
            gc.delete_event(e.id)
    else:
        for calendar in gc.get_calendar_list():
            if calendar.summary == "Study":
                gc.delete_calendar(calendar.id)
                print(f"Deleted old calendar: {calendar.id}")

        calendar_id = gc.add_calendar(GCSACalendar("Study")).calendar_id
        gc = GoogleCalendar(calendar_id, open_browser=open_browser)
        print(f"Created new calendar: {calendar_id}")

    tz = timezone(gc.get_settings().timezone)

    for e in load_ics_events(ics_path):
        desc = e.description or ""
        if "odwołane" in desc:
            continue

        location = extract_location(desc)
        summary = f"{location} {e.name}".strip()
        cleaned_desc = clean_description(desc)

        start = tz.localize(e.begin.datetime.replace(tzinfo=None))
        end = tz.localize(e.end.datetime.replace(tzinfo=None))

        gc.add_event(
            Event(
                summary=summary,
                start=start,
                end=end,
                description=cleaned_desc,
                color_id=determine_color(desc),
            )
        )


def ics_edit(
    input_path: str = "Plany.ics",
    output_path: str = "Plany_edited.ics",
    timezone_str: str = "Europe/Warsaw",
):
    """
    Edits the events in an ICS file by extracting relevant details and adjusting the time zone.

    Parameters:
    - input_path (str): Path to the input ICS file.
    - output_path (str): Path to the output edited ICS file.
    - timezone_str (str): The time zone to apply to event times.

    Algorithm:
    1. Loads events from the ICS file.
    2. Extracts and cleans event details (location, description).
    3. Localizes the event start and end times to the specified time zone.
    4. Writes the updated events to a new ICS file.

    The function will ensure that the output directory exists and the updated calendar is written to the specified path.
    """
    events = load_ics_events(input_path)
    new_cal = ICSCalendar()
    tz = timezone(timezone_str)

    for e in events:
        if "odwołane" in (e.description or ""):
            continue
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
        )
        new_cal.events.add(new_event)

    # Ensure the directory exists for the output file
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Write the updated calendar to the output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(new_cal.serialize_iter())
