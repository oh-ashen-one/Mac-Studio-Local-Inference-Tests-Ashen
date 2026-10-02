import re

def valid_date(date):
    """
    Validates a given date string according to specific rules:
    1. The date string is not empty.
    2. The number of days is valid for the given month (considering leap years for February).
    3. The month is between 1 and 12.
    4. The date is in the format: mm-dd-yyyy
    
    Returns True if valid, False otherwise.
    """
    # Rule 1: Check if the date string is not empty
    if not date or not isinstance(date, str) or date.strip() == '':
        return False
    
    # Rule 4: Check the format mm-dd-yyyy
    # Use regex to match the format
    pattern = r'^(\d{2})-(\d{2})-(\d{4})$'
    match = re.match(pattern, date)
    if not match:
        return False
    
    month_str = match.group(1)
    day_str = match.group(2)
    year_str = match.group(3)
    
    # Convert to integers
    try:
        month = int(month_str)
        day = int(day_str)
        year = int(year_str)
    except ValueError:
        return False
    
    # Rule 3: Month should be between 1 and 12
    if month < 1 or month > 12:
        return False
    
    # Rule 2: Validate days based on month
    # Days in each month
    days_in_month = {
        1: 31, 3: 31, 5: 31, 7: 31, 8: 31, 10: 31, 12: 31,
        4: 30, 6: 30, 9: 30, 11: 30,
        2: 28  # Default, will adjust for leap years
    }
    
    # Check for leap year for February
    if month == 2:
        # Leap year: divisible by 4, but not by 100 unless also by 400
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            max_days = 29
        else:
            max_days = 28
    else:
        max_days = days_in_month[month]
    
    # Day must be between 1 and max_days
    if day < 1 or day > max_days:
        return False
    
    return True
