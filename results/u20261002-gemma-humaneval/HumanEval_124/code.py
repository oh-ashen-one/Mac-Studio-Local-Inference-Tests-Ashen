import datetime

def valid_date(date):
    """You have to write a function which validates a given date string and
    returns True if the date is valid otherwise False.
    The date is valid if all of the following rules are satisfied:
    1. The date string is not empty.
    2. The number of days is not less than 1 or higher than 31 days for months 1,3,5,7,8,10,12. And the number of days is not less than 1 or higher than 30 days for months 4,6,9,11. And, the number of days is not less than 1 or higher than 29 for the month 2.
    3. The months should not be less than 1 or higher than 12.
    4. The date should be in the format: mm-dd-yyyy
    """
    if not date:
        return False
    
    parts = date.split('-')
    if len(parts) != 3:
        return False
    
    # Ensure parts have correct lengths to strictly follow mm-dd-yyyy format
    if len(parts[0]) != 2 or len(parts[1]) != 2 or len(parts[2]) != 4:
        return False
        
    try:
        month = int(parts[0])
        day = int(parts[1])
        year = int(parts[2])
    except ValueError:
        return False

    if not (1 <= month <= 12):
        return False

    # Rule 2: Specific day limits per month
    if month in [1, 3, 5, 7, 8, 10, 12]:
        if not (1 <= day <= 31):
            return False
    elif month in [4, 6, 9, 11]:
        if not (1 <= day <= 30):
            return False
    elif month == 2:
        if not (1 <= day <= 29):
            return False
            
    return True
