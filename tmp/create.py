from random import choice
from gcsa.google_calendar import GoogleCalendar
from gcsa.calendar import Calendar

gc = GoogleCalendar(open_browser=False)

calendar_name = "Study_" + choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
gc = GoogleCalendar(open_browser=False)
calendar = gc.add_calendar(Calendar(calendar_name))