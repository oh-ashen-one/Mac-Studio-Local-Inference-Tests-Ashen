import re

def valid_date(date):
    if not date:
        return False

    if not re.fullmatch(r'\d{2}-\d{2}-\d{4}', date):
        return False

    try:
        month, day, year = map(int, date.split('-'))
    except ValueError:
        return False

    if month < 1 or month > 12:
        return False

    if day < 1:
        return False

    if month in {1, 3, 5, 7, 8, 10, 12}:
        max_days = 31
    elif month in {4, 6, 9, 11}:
        max_days = 30
    else:  # February
        max_days = 29

    if day > max_days:
        return False

    return True
