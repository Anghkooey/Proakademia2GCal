import re
from datetime import datetime
import pandas as pd
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar


def main():
    """
    Main function that processes a CSV file containing event data and imports the events into a Google Calendar.

    This function performs the following tasks:
    1. Loads event data from a CSV file ('Plany.Csv').
    2. Extracts the event date and time, group, subject, teacher, and notes from the CSV file.
    3. Creates event descriptions based on the extracted data.
    4. Skips events that are marked as 'odwołane' (canceled).
    5. Adds the processed events to Google Calendar using the gcsa library.

    The function performs the following steps:
    - Reads the CSV file while handling specific encoding and ensuring empty cells are not treated as missing.
    - Parses each row to extract event details using regular expressions.
    - Converts the extracted start and end times into datetime objects.
    - Creates an event description that includes group, subject, teacher, and any additional notes.
    - For each valid event, the script creates a Google Calendar event and adds it to the specified Google Calendar.

    The function also handles the case where the CSV contains a line specifying the event date, which is used to associate the event with the correct date.
    """
    # Initialize GoogleCalendar instance
    gc = GoogleCalendar()

    # Load CSV data into a DataFrame, ignoring default missing values
    df = pd.read_csv(
        "Plany.Csv",
        header=None,
        skiprows=1,
        encoding="windows-1250",
        keep_default_na=False,
    )

    # Variable to store the current date
    current_date = None

    # Regular expression pattern for matching event details in the CSV
    event_pattern = re.compile(
        r";(\d{1,2}:\d{2});(\d{1,2}:\d{2});[^;]*;([^;]*);([^;]*);[^;]*;([^;]*);[^;]*;(.*)"
    )

    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        # Join row values, excluding empty strings
        line = ";".join(str(x).strip() for x in row if x != "")

        # Check for the line indicating the date of the event
        if "Data Zajęć:" in line:
            match = re.search(r"Data Zajęć:\s*(\d{4}\.\d{2}\.\d{2})", line)
            if match:
                # Parse the date from the CSV and set it as the current date
                current_date = datetime.strptime(match.group(1), "%Y.%m.%d").date()

        # Match the line containing event details (start time, end time, group, etc.)
        elif match := event_pattern.match(line):
            start_str, end_str, group, subject, teacher, notes = match.groups()

            # Skip the event if it has been canceled
            if re.search(r"odwołane", notes, re.IGNORECASE):
                continue

            # Combine the parsed date with the start and end times to create datetime objects
            start_dt = datetime.combine(
                current_date, datetime.strptime(start_str, "%H:%M").time()
            )
            end_dt = datetime.combine(
                current_date, datetime.strptime(end_str, "%H:%M").time()
            )

            # Construct a detailed event description
            description = f"{group}\n{subject}\n{teacher}\n{notes.strip()}"

            # Create an Event object and add it to Google Calendar
            event = Event(
                summary=subject, start=start_dt, end=end_dt, description=description
            )
            gc.add_event(event)


if __name__ == "__main__":
    main()
