import argparse
import json
import re
import sys
from datetime import datetime
from uuid import uuid4
from itertools import islice
from pathlib import Path

from ics import Calendar, Event


def load_schedule(path: str) -> list:
    """
    Loads schedule events from a JSON file.

    First attempts to parse the whole file.
    If that fails, attempts to parse the JSON object on line 13.
    """
    with open(path, encoding="utf-8") as file:
        content = file.read()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        lines = content.splitlines()
        line = next(islice(lines, 12, 13), None)

        if line is None:
            raise ValueError(
                f"{path}: the file contains fewer than 13 lines."
            )

        try:
            data = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"{path}: could not parse JSON or JSON on line 13."
            ) from exc

    try:
        return data["result"]["classScheduleGroups"]
    except (KeyError, TypeError) as exc:
        raise ValueError(
            f"{path}: invalid JSON format. "
            "'result.classScheduleGroups' was not found."
        ) from exc


def parse_datetime(date: str, time: str) -> datetime:
    """Combines date and time from the JSON schedule."""
    date_part = date.split("T")[0]
    return datetime.fromisoformat(f"{date_part}T{time}")


def polish_weekday(dt: datetime) -> str:
    """Returns the Polish weekday name."""
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
    """Formats date like the original ICS description."""
    return f"{dt:%Y.%m.%d} {polish_weekday(dt)}"


def calculate_duration(start: datetime, end: datetime) -> str:
    """Calculates duration in hours and minutes."""
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

        # Remove "- Lab" from the room description.
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

    # Location has the highest priority.
    if "pracownia informatyczna" in location:
        return "Lab"

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

    if form in ("lecture", "foreign language course"):
        return "Wyk"

    if "laboratory" in form:
        return "Lab"

    return ""


def get_form_number(item: dict) -> str:
    """
    Returns the original numeric value for 'Forma zajęć',
    if the JSON explicitly contains it.
    """
    return str(item.get("formNumber", ""))


def build_description(
    item: dict,
    start: datetime,
    end: datetime,
) -> str:
    """Builds a description similar to the original Proakademia ICS."""

    name = item.get("name", "")
    lecturer = item.get("lecturer", "")
    comments = item.get("comments") or ""
    label_text = item.get("labelText") or ""

    location = clean_location(item.get("location", ""))
    duration = calculate_duration(start, end)
    group_type = get_group_type(item)

    return (
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


def create_event(item: dict) -> Event:
    """Converts one JSON schedule item into an ICS event."""

    start = parse_datetime(item["date"], item["hourFrom"])
    end = parse_datetime(item["date"], item["hourTo"])

    name = item.get("name", "Unknown subject")
    description = build_description(item, start, end)

    return Event(
        name=name,
        begin=start,
        end=end,
        description=description,
        uid=str(uuid4()),
    )


def natural_sort_key(path: Path):
    """
    Sorts numbered files numerically:
    1.json, 2.json, 3.json, 10.json.
    """
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", path.name)
    ]


def get_input_files(input_paths: list[str]) -> list[Path]:
    """
    Resolves input arguments into a list of JSON files.

    Directories: include JSON files and files with numeric names.
    Explicit files: include the supplied files.
    """
    files = []

    for raw_path in input_paths:
        path = Path(raw_path)

        if not path.exists():
            raise FileNotFoundError(f"Input path not found: {path}")

        if path.is_dir():
            candidates = [
                child
                for child in path.iterdir()
                if child.is_file()
                and (
                    child.suffix.lower() == ".json"
                    or child.stem.isdigit()
                )
            ]

            candidates.sort(key=natural_sort_key)
            files.extend(candidates)

        elif path.is_file():
            files.append(path)

    # Remove duplicate paths while preserving order.
    unique_files = []
    seen = set()

    for file in files:
        resolved = file.resolve()

        if resolved not in seen:
            seen.add(resolved)
            unique_files.append(file)

    if not unique_files:
        raise ValueError(
            "No input files found. "
            "Provide a JSON file or a directory containing JSON files."
        )

    return unique_files


def pcap(
    input_path: str | list[str] = "pc.json",
    output_path: str = "Plany.ics",
):
    """
    Converts one or more JSON schedules into a single ICS calendar.
    """
    input_paths = (
        [input_path]
        if isinstance(input_path, str)
        else input_path
    )

    files = get_input_files(input_paths)
    calendar = Calendar()

    total_events = 0

    for file_path in files:
        schedule = load_schedule(str(file_path))

        for item in schedule:
            calendar.events.add(create_event(item))
            total_events += 1

        print(f"📄 Loaded {len(schedule)} events from {file_path}")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as file:
        file.writelines(calendar.serialize_iter())

    print(
        "\n✅ PCAP conversion completed successfully!"
        f"\n📁 Input files: {len(files)}"
        f"\n📅 Total events: {total_events}"
        f"\n📁 Output: {output}"
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Converts one or more Proakademia JSON schedules "
            "into a single ICS calendar."
        )
    )

    parser.add_argument(
        "input_paths",
        nargs="*",
        default=None,
        help=(
            "Input JSON file(s) or folder(s). "
            "Defaults to pc.json."
        ),
    )

    parser.add_argument(
        "-o",
        "--output_path",
        default="Plany.ics",
        help="Output ICS path. Defaults to Plany.ics.",
    )

    args = parser.parse_args()
    input_paths = args.input_paths or ["pc.json"]

    try:
        pcap(
            input_path=input_paths,
            output_path=args.output_path,
        )
    except Exception as exc:
        print(f"❌ An error occurred during conversion: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()