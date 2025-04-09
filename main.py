from datetime import datetime, timedelta
from ics import Calendar
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from config import calendar_id
from pytz import timezone

# TODO: time logs

COLOR = {
    'Lab': '7',
    'Cw': '10',
    'Uwagi': '11',
    'Online_or_Cancelled': '3',
    'Default': '8'
}

gc = GoogleCalendar(calendar_id)
tz = timezone(gc.get_settings().timezone)

cutoff = datetime.now() - timedelta(days=30)
for e in gc.get_events(time_min=cutoff):
    gc.delete_event(e.id)

with open('Plany.ics', encoding='utf-8') as f:
    events = Calendar(f.read()).events

for e in events:
    desc = e.description or ''
    if 'odwołane' in desc:
        continue

    color_id = COLOR['Default']
    if "Uwagi: \n" not in desc:
        color_id = COLOR['Uwagi']
    elif "Sala: \n" in desc:
        color_id = COLOR['Online_or_Cancelled']
    elif "Grupy: Lab" in desc:
        color_id = COLOR['Lab']
    elif "Grupy: Cw" in desc:
        color_id = COLOR['Cw']

    start = tz.localize(e.begin.datetime.replace(tzinfo=None))
    end = tz.localize(e.end.datetime.replace(tzinfo=None))

    gc.add_event(Event(
        summary=e.name,
        start=start,
        end=end,
        description=desc,
        color_id=color_id
    ))
