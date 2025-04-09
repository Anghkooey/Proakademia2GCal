from random import randint
from datetime import datetime
from gcsa.google_calendar import GoogleCalendar
from gcsa.calendar import Calendar

calendar_name = f"Study_{datetime.now():%d%m%Y}_{randint(0, 1000)}"
gc = GoogleCalendar(open_browser=False)
print(gc.add_calendar(Calendar(calendar_name)).calendar_id)