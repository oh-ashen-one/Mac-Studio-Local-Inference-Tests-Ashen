def closest_integer(value):
    '''
    Create a function that takes a value (string) representing a number
    and returns the closest integer to it. If the number is equidistant
    from two integers, round it away from zero.

    Examples
    >>> closest_integer("10")
    10
    >>> closest_integer("15.3")
    15

    Note:
    Rounding away from zero means that if the given number is equidistant
    from two integers, the one you should return is the one that is the
    farthest from zero. For example closest_integer("14.5") should
    return 15 and closest_integer("-14.5") should return -15.
    '''
    num = float(value)
    # Get the floor and ceiling
    floor_val = int(num)
    ceil_val = floor_val + 1
    
    # If num is negative, floor is more negative, ceil is less negative
    # For positive: floor is smaller, ceil is larger
    
    # Check which is closer
    diff_floor = abs(num - floor_val)
    diff_ceil = abs(num - ceil_val)
    
    if diff_floor < diff_ceil:
        return floor_val
    elif diff_ceil < diff_floor:
        return ceil_val
    else:
        # Equidistant: round away from zero
        if num >= 0:
            return ceil_val
        else:
            return floor_val
