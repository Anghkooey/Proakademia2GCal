from datetime import datetime, timedelta
from ics import Calendar as ICSCalendar
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.calendar import Calendar as GCSACalendar
from pytz import timezone
import re

def ics_import(calendar_id: str = None, ics_path: str = "Plany.ics", open_browser: bool = True):
    """
    Imports events from an ICS file into a specified Google Calendar. If no calendar_id is provided, 
    a new calendar named 'Study' will be created. Old events (older than 30 days) are deleted from the 
    calendar before importing new events.

    Parameters:
    - calendar_id (str): The ID of the existing Google Calendar to import events into. If not provided, 
                          a new calendar will be created and used.
    - ics_path (str): The path to the ICS file containing the events to import. Defaults to "Plany.ics".
    - open_browser (bool): Flag to indicate whether the browser should be opened for Google authentication. 
                           Defaults to True.

    Algorithm:
    1. Check if `calendar_id` is provided. If so, use the existing calendar. 
       If not, search for an existing 'Study' calendar, delete it if found, 
       and create a new 'Study' calendar.
    2. Set the timezone based on the Google Calendar settings.
    3. Delete any old events from the last 30 days from the calendar.
    4. Open the provided ICS file and parse the events.
    5. For each event:
       - Skip events with descriptions containing "odwołane".
       - Based on the event description, determine the appropriate color for the event (Exam, Online, etc.).
       - Extract the location (Sala) from the description if available.
       - Parse the event's start and end times and localize them to the calendar's timezone.
       - Clean the description, keeping only relevant lines (Sala, Uwagi, Prowadzący).
       - Add the event to the Google Calendar.
    
    The function will print the ID of the created calendar or the ID of the existing calendar being used.
    """

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

    keep_pattern = re.compile(r"^(Sala|Uwagi|Prowadzący):\s*\S+")
    
    gc = GoogleCalendar(open_browser=open_browser)

    # Check if a calendar ID is provided
    if calendar_id:
        # If the current calendar matches the provided calendar ID (i.e., using the primary calendar)
        if gc.get_calendar().id == gc.get_calendar(calendar_id).id:
            
            # Prompt the user with a warning message about deleting all existing events
            user_confirmation = input("You are about to use your primary calendar. All existing events will be deleted. Are you sure you want to proceed? (yes/no): ")
            
            if user_confirmation.lower() != 'yes':
                print("Operation aborted.")
                
                # Exit the program to prevent any changes to the calendar
                exit()

        gc = GoogleCalendar(calendar_id)
    else:
        for calendar in GoogleCalendar().get_calendar_list():
            if calendar.summary == "Study":
                gc.delete_calendar(calendar.id)
                print(f"Deleted old calendar: {calendar.id}")

        calendar_id = gc.add_calendar(GCSACalendar("Study")).calendar_id
        print(f"Created new calendar: {calendar_id}")
        gc = GoogleCalendar(calendar_id, open_browser=open_browser)

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
            # Exam
            color_id = COLORS["Tomato"]
        elif "Sala: \n" in desc:
            # Online or cancelled
            color_id = COLORS["Grape"]
        elif "Grupy: Wyk" in desc:
            color_id = COLORS["Graphite"]
        elif any(k in desc for k in ["Grupy: Cw", "Grupy: Lek"]):
            color_id = COLORS["Basil"]
        elif "Grupy: Lab" in desc:
            color_id = COLORS["Peacock"]
        else:
            # Unknown
            color_id = COLORS["Banana"]

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
