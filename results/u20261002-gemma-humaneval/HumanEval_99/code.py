import decimal

def closest_integer(value):
    '''
    Create a function that takes a value (string) representing a number
    and returns the closest integer to it. If the number is equidistant
    from two integers, round it away from zero.
    '''
    # Use decimal module to handle precision and specific rounding modes
    # ROUND_HALF_UP rounds towards the nearest neighbor. 
    # If equidistant, it rounds away from zero for positive numbers.
    # However, for negative numbers, ROUND_HALF_UP rounds -14.5 to -14.
    # To achieve "round away from zero" for both signs, we use ROUND_HALF_UP 
    # on the absolute value and restore the sign.
    
    d = decimal.Decimal(value)
    sign = 1 if d >= 0 else -1
    abs_d = abs(d)
    
    # Quantize to integer using ROUND_HALF_UP (rounds .5 up to 1)
    rounded = abs_d.quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_UP)
    
    return int(rounded) * sign
