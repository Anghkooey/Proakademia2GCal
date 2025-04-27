import os
import re
from datetime import datetime, timedelta
from typing import List, Optional

from gcsa.calendar import Calendar as GCSACalendar
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from google.auth.exceptions import RefreshError
from ics import Calendar as ICSCalendar
from ics import Event as ICSEvent
from pytz import timezone
from tqdm import tqdm

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
    if all(x not in desc for x in ("Uwagi: \n", "obieralny", "Online")):
        return COLORS["Tomato"]  # Exam
    elif any(x in desc for x in ("Sala: \n", "Online")):
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
    _retry: bool = False,
):
    """
    Imports events from an ICS file into a Google Calendar, either by updating an existing calendar or creating a new one.

    This function handles expired or revoked OAuth tokens automatically: if authentication fails due to an invalid token,
    the token file (`~/.credentials/token.pickle`) will be deleted and the function will retry once.

    Parameters:
    ----------
    calendar_id : Optional[str], default=None
        The ID of the target Google Calendar to import events into.
        If None, the function will search for an existing "Study" calendar or create a new one.

    ics_path : str, default="Plany.ics"
        Path to the ICS (iCalendar) file containing the events to import.

    open_browser : bool, default=True
        If True, opens a browser window for OAuth authentication when needed.
        If False, attempts to authenticate silently using existing credentials.

    _retry : bool, default=False
        Internal flag to prevent infinite retry loops.
        Should not be modified manually when calling the function.

    Workflow:
    ---------
    1. Attempt to authenticate using stored credentials.
    2. If `calendar_id` is provided, validate and select the specified calendar.
    3. If no `calendar_id`, check for an existing "Study" calendar:
        - If found, delete it and create a new one.
        - If not found, create a new calendar named "Study."
    4. Clean the calendar:
        - Fetch and delete all events older than 30 days.
    5. Parse and load events from the provided ICS file.
    6. For each event:
        - Adjust timezones based on Google Calendar settings.
        - Extract location and clean event description.
        - Assign a color based on the event type (Lecture, Exam, Seminar, etc.).
        - Import the event into the selected Google Calendar.
    7. If token is expired or revoked:
        - Delete the corrupted token file.
        - Retry authentication and import once.

    Raises:
    -------
    google.auth.exceptions.RefreshError
        If authentication fails even after attempting to delete and refresh the credentials.

    Notes:
    ------
    - Token expiration is detected and handled automatically.
    - Protects users from accidentally deleting their primary Google Calendar.
    - This function is designed to be idempotent: if rerun with the same ICS file and calendar, it will refresh events cleanly.
    - Timezone handling ensures consistency between event times in the ICS file and the target Google Calendar.

    """
    try:
        gc = GoogleCalendar(open_browser=open_browser)

        if calendar_id:
            if gc.get_calendar().id == gc.get_calendar(calendar_id).id:
                confirmation = input(
                    "⚠️ You’re about to delete your primary calendar. Proceed? (yes/no): "
                )
                if confirmation.lower() != "yes":
                    print("🚫 Operation aborted.")
                    exit()
            gc = GoogleCalendar(calendar_id)

            events_to_delete = list(
                gc.get_events(time_min=(datetime.now() - timedelta(days=30)))
            )
            for e in tqdm(
                events_to_delete,
                total=len(events_to_delete),
                desc="🗑️ Deleting old events",
                ncols=80,
                colour="MAGENTA",
                leave=False,
            ):
                gc.delete_event(e.id)
            print("✅ Completed: 🗑️  Delete old events")
        else:
            for calendar in gc.get_calendar_list():
                if calendar.summary == "Study":
                    gc.delete_calendar(calendar.id)
                    print(f"🗑️ Old calendar deleted: {calendar.id}")

            calendar_id = gc.add_calendar(GCSACalendar("Study")).calendar_id
            gc = GoogleCalendar(calendar_id, open_browser=open_browser)
            print(f"✅ New calendar created: {calendar_id}")

        tz = timezone(gc.get_settings().timezone)

        ics_events = list(load_ics_events(ics_path))
        for e in tqdm(
            ics_events,
            total=len(ics_events),
            desc="📅 Importing new events",
            ncols=80,
            colour="CYAN",
            leave=False,
        ):
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
        print("✅ Completed: 📅 Import new events")

    except RefreshError as e:
        if not _retry:
            print("⚠️ Detected invalid or expired token. Removing token and retrying...")
            token_path = os.path.expanduser("~/.credentials/token.pickle")
            if os.path.exists(token_path):
                os.remove(token_path)
                print(f"🗑️ Deleted token file: {token_path}")
            else:
                print(f"⚠️ Token file not found at: {token_path}")

            ics_import(calendar_id, ics_path, open_browser, _retry=True)
        else:
            print("❌ Failed to refresh credentials even after retrying.")
            raise e


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
    print(f"✅ ICS editing completed successfully!\n📁 Output saved to: {output_path}")
