from datetime import datetime, timedelta, time
from django.utils import timezone

def generate_time_slots(start_date, end_date):
    slots = []
    current_date = start_date

    while current_date <= end_date:
        weekday = current_date.weekday()

        if weekday < 5:  # Пн–Пт
            # Утро: 9:00–13:00
            start = time(9, 0)
            end = time(13, 0)
            slots += _create_slots_for_day(current_date, start, end)

            # После обеда: 14:30–19:00
            start = time(14, 30)
            end = time(19, 0)
            slots += _create_slots_for_day(current_date, start, end)

        elif weekday == 5:  # Суббота
            start = time(9, 0)
            end = time(14, 0)
            slots += _create_slots_for_day(current_date, start, end)

        # Воскресенье – выходной
        current_date += timedelta(days=1)

    return slots

def _create_slots_for_day(date, start_time, end_time):
    slots = []
    dt = datetime.combine(date, start_time)
    end_dt = datetime.combine(date, end_time)

    while dt < end_dt:
        slots.append(timezone.make_aware(dt))
        dt += timedelta(minutes=30)

    return slots
