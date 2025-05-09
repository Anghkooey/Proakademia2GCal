import sys
import argparse
import tkinter as tk
from tkinter import filedialog
import os
import re
from ics import Calendar as ICSCalendar
from ics import Event as ICSEvent
from pytz import timezone

# Regex pattern to extract certain lines from descriptions (Sala, Uwagi, Prowadzący)
KEEP_PATTERN = re.compile(r"^(Sala|Uwagi|Prowadzący|Grupy):\s*\S+")


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


def load_ics_events(path: str) -> list:
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
    1. Loads events from the ICS file using load_ics_events.
    2. Extracts and cleans event details (location, description) using extract_location and clean_description.
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


def main():
    """
    Entry point for the ICS editing utility.

    This function parses command-line arguments for specifying the input file,
    output file, and timezone. If no input file is provided via arguments,
    it opens a file selection dialog to allow the user to choose an .ics file.
    It then calls the core 'ics_edit' function with the obtained parameters.

    Handles command-line arguments using argparse and falls back to a Tkinter
    file dialog if the input file path is not provided.
    """
    # Set up argument parser for command-line interaction.
    # RawTextHelpFormatter is used to preserve formatting in the help message.
    parser = argparse.ArgumentParser(
        description="Edits an ICS (iCalendar) file. Cleans event descriptions, "
        "extracts relevant information (like location), and adjusts "
        "event times based on the specified timezone.\n\n"
        "If INPUT_PATH is not provided, a file selection dialog will open.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Define the positional argument for the input file path.
    # It's made optional (nargs='?') so the script can run without arguments
    # to trigger the file dialog.
    parser.add_argument(
        "input_path",
        nargs="?",  # Makes the argument optional
        help="Path to the input .ics file.",
    )

    # Define an optional argument for the output file path.
    # Provides a default value if not specified by the user.
    parser.add_argument(
        "-o",
        "--output_path",
        default="Plany_edited.ics",
        help="Path to save the edited .ics file.\n"
        "Defaults to 'Plany_edited.ics' in the current directory.",
    )

    # Define an optional argument for the timezone string.
    # Provides a default timezone (Warsaw) if not specified.
    parser.add_argument(
        "-t",
        "--timezone",
        default="Europe/Warsaw",
        help="Timezone to apply to event times (e.g., 'UTC', 'America/New_York').\n"
        "Defaults to 'Europe/Warsaw'.",
    )

    # argparse automatically adds a -h/--help argument based on the description.

    # Parse the command-line arguments provided by the user.
    args = parser.parse_args()

    # Determine the input file path. Prioritize the command-line argument.
    input_file = args.input_path

    # If no input path was provided via command line arguments, open the file dialog.
    if not input_file:
        print("Input file path not specified. Opening file selection dialog...")
        # Initialize Tkinter root window but immediately hide it.
        # This prevents a blank Tkinter window from appearing behind the dialog.
        root = tk.Tk()
        root.withdraw()

        # Open the file dialog, filtering for .ics files.
        input_file = filedialog.askopenfilename(
            initialdir=".",  # Start Browse from the current directory
            title="Select an ICS file to edit",
            filetypes=(("ICS files", "*.ics"), ("All files", "*.*")),
        )

        # Destroy the hidden root window after the dialog is closed.
        root.destroy()

    # Proceed only if an input file was successfully obtained (either from args or dialog).
    if input_file:
        # Confirm the selected parameters to the user.
        print(f"Selected input file: {input_file}")
        print(f"Output file will be saved as: {args.output_path}")
        print(f"Applying timezone: {args.timezone}")

        try:
            # Call the core ICS editing logic.
            ics_edit(
                input_path=input_file,
                output_path=args.output_path,
                timezone_str=args.timezone,
            )
        except Exception as e:
            # Catch any exceptions that occur during the ICS processing
            # and report them to the user.
            print(f"An error occurred during file processing: {e}")
            sys.exit(1)  # Exit with a non-zero status code

    else:
        # If input_file is still None, it means the user closed the file dialog
        # without selecting a file.
        print("No ICS file selected. Exiting program.")
        sys.exit(0)  # Exit cleanly as the user chose not to proceed


# Standard Python entry point check. Ensures the main function is called
# when the script is executed directly.
if __name__ == "__main__":
    main()
