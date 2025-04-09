from main import gc

from gcsa.calendar import Calendar

calendar = Calendar(
    'Travel calendar'
)
calendar = gc.add_calendar(calendar)

# for calendar in  gc.get_events():
#     print(calendar)
