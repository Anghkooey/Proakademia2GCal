import re
from datetime import datetime
import pandas as pd
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar

gc = GoogleCalendar("7c5156a93572910b71669772b6800327712337d39e25e1fb2d04ae8b626d7ba8@group.calendar.google.com")

df = pd.read_csv('Plany.Csv', header=None, skiprows=1, encoding='windows-1250', keep_default_na=False)

current_date = None
event_pattern = re.compile(r';(\d{1,2}:\d{2});(\d{1,2}:\d{2});[^;]*;([^;]*);([^;]*);[^;]*;([^;]*);[^;]*;(.*)')

for _, row in df.iterrows():
    line = ';'.join(str(x).strip() for x in row if x != '')

    if 'Data Zajęć:' in line:
        match = re.search(r'Data Zajęć:\s*(\d{4}\.\d{2}\.\d{2})', line)
        if match:
            current_date = datetime.strptime(match.group(1), "%Y.%m.%d").date()
    elif match := event_pattern.match(line):
        start_str, end_str, group, subject, teacher, notes = match.groups()
        if re.search(r'odwołane', notes, re.IGNORECASE):
            continue

        start_dt = datetime.combine(current_date, datetime.strptime(start_str, "%H:%M").time())
        end_dt = datetime.combine(current_date, datetime.strptime(end_str, "%H:%M").time())
        description = f"{group}\n{subject}\n{teacher}\n{notes.strip()}"
        event = Event(summary=subject, start=start_dt, end=end_dt, description=description)
        gc.add_event(event)
