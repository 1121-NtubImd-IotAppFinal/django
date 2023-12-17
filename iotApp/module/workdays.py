from datetime import timedelta, date

def get_workdays(start_date, end_date):
    workdays = 0
    delta = timedelta(days=1)
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() < 5:
            workdays += 1
        current_date += delta

    return workdays
