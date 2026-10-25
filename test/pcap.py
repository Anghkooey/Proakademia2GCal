import argparse
import json
import os
import re
import sys
from datetime import datetime
from uuid import uuid4

from ics import Calendar, Event

from itertools import islice


def load_schedule(path: str) -> list:
    """Load schedule events from the JSON object on line 13."""
    with open(path, encoding="utf-8") as file:
        line = next(islice(file, 12, 13), None)

    if line is None:
        raise ValueError("The file contains fewer than 13 lines.")

    data = json.loads(line)

    try:
        return data["result"]["classScheduleGroups"]
    except KeyError as exc:
        raise ValueError(
            "Invalid JSON format: 'result.classScheduleGroups' was not found."
        ) from exc

def parse_datetime(date: str, time: str) -> datetime:
    """
    Combines date and time from the JSON schedule.
    """
    date_part = date.split("T")[0]
    return datetime.fromisoformat(f"{date_part}T{time}")


def polish_weekday(dt: datetime) -> str:
    """
    Returns the Polish weekday name.
    """
    weekdays = {
        0: "poniedziałek",
        1: "wtorek",
        2: "środa",
        3: "czwartek",
        4: "piątek",
        5: "sobota",
        6: "niedziela",
    }

    return weekdays[dt.weekday()]


def format_date(dt: datetime) -> str:
    """
    Formats date in the same style as the original ICS file.
    """
    return f"{dt:%Y.%m.%d} {polish_weekday(dt)}"


def calculate_duration(start: datetime, end: datetime) -> str:
    """
    Calculates duration in hours and minutes.
    """
    total_minutes = int((end - start).total_seconds() // 60)

    hours = total_minutes // 60
    minutes = total_minutes % 60

    return f"{hours}h{minutes:02d}m"


def clean_location(location: str) -> str:
    if not location:
        return ""

    locations = []

    for part in location.split(","):
        part = re.sub(r"\s+", " ", part).strip()

        # bud.A A 125 -> bud.A 125
        part = re.sub(
            r"\bbud\.([A-Za-zĄĆĘŁŃÓŚŹŻ])\s+\1\b",
            r"bud.\1",
            part,
            flags=re.IGNORECASE,
        )

        # PRACOWNIA INFORMATYCZNA -> Lab
        part = re.sub(
            r"\bpracownia\s+informatyczna\b",
            "Lab",
            part,
            flags=re.IGNORECASE,
        )

        # " - Lab" убираем из Sala
        part = re.sub(
            r"\s*-\s*Lab\b",
            "",
            part,
            flags=re.IGNORECASE,
        )

        part = re.sub(r"\s+", " ", part).strip()

        if part:
            locations.append(part)

    return ", ".join(locations)

def get_group_type(item: dict) -> str:
    location = (item.get("location") or "").lower()
    group = (item.get("group") or "").upper()
    form = (item.get("form") or "").lower()

    # LOCATION — highest priority
    if "pracownia informatyczna" in location:
        return "Lab"

    # GROUP
    if "LAB" in group:
        return "Lab"

    if "WYK" in group:
        return "Wyk"

    if "LEK" in group:
        return "Lek"

    if "CW" in group:
        return "Cw"

    if "KON" in group:
        return "Kon"

    # FORM
    if form in ("lecture", "foreign language course"):
        return "Lek"

    if "laboratory" in form:
        return "Lab"

    return ""

def get_form_number(item: dict) -> str:
    """
    Returns the value for 'Forma zajęć'.

    The JSON does not contain the original numeric value,
    so an empty string is returned unless 'formNumber'
    is explicitly present.
    """
    return str(item.get("formNumber", ""))



def build_description(
    item: dict,
    start: datetime,
    end: datetime,
) -> str:
    """
    Builds a description similar to the original Proakademia ICS file.
    """

    name = item.get("name", "")
    lecturer = item.get("lecturer", "")
    comments = item.get("comments") or ""
    label_text = item.get("labelText") or ""

    # Clean location before putting it into the ICS file.
    location = clean_location(
        item.get("location", "")
    )

    duration = calculate_duration(start, end)
    group_type = get_group_type(item)

    description = (
        f"Data zajęć: {format_date(start)}\n"
        f"Czas od: {start:%H:%M}\n"
        f"Czas do: {end:%H:%M}\n"
        f"Liczba godzin: {duration}\n"
        f"Przedmiot: {name}\n"
        f"Forma zajęć: {get_form_number(item)}\n"
        f"Grupy: {group_type}\n"
        f"Sala: {location}\n"
        f"Prowadzący: {lecturer}\n"
        f"Forma zaliczenia: \n"
        f"Uwagi: {label_text or comments}"
    )

    return description

def create_event(item: dict) -> Event:
    """
    Converts one JSON schedule item into an ICS event.
    """

    start = parse_datetime(
        item["date"],
        item["hourFrom"],
    )

    end = parse_datetime(
        item["date"],
        item["hourTo"],
    )

    name = item.get(
        "name",
        "Unknown subject",
    )

    description = build_description(
        item,
        start,
        end,
    )

    return Event(
        name=name,
        begin=start,
        end=end,
        description=description,
        uid=str(uuid4()),
    )


def pcap(
    input_path: str = "pc.json",
    output_path: str = "Plany.ics",
):
    """
    Converts pc.json into Plany.ics.
    """

    schedule = load_schedule(input_path)

    calendar = Calendar()

    for item in schedule:
        event = create_event(item)
        calendar.events.add(event)

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as f:
        f.writelines(
            calendar.serialize_iter()
        )

    print(
        "✅ PCAP conversion completed successfully!"
        f"\n📁 Input: {input_path}"
        f"\n📁 Output: {output_path}"
        f"\n📅 Events: {len(schedule)}"
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Converts a Proakademia schedule JSON "
            "file into an ICS calendar file."
        )
    )

    parser.add_argument(
        "input_path",
        nargs="?",
        default="pc.json",
        help=(
            "Path to the input JSON file. "
            "Defaults to 'pc.json'."
        ),
    )

    parser.add_argument(
        "-o",
        "--output_path",
        default="Plany.ics",
        help=(
            "Path to the output ICS file. "
            "Defaults to 'Plany.ics'."
        ),
    )

    args = parser.parse_args()

    try:
        pcap(
            input_path=args.input_path,
            output_path=args.output_path,
        )
    except Exception as e:
        print(
            f"❌ An error occurred during conversion: {e}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
