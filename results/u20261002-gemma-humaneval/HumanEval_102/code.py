def choose_num(x, y):
    """This function takes two positive numbers x and y and returns the
    biggest even integer number that is in the range [x, y] inclusive. If 
    there's no such number, then the function should return -1.

    For example:
    choose_num(12, 15) = 14
    choose_num(13, 12) = -1
    """
    if x > y:
        return -1
    
    # Start from the upper bound and go downwards to find the first even number
    # We use int() to ensure we are dealing with integers if floats are passed
    upper = int(y)
    lower = int(x)
    
    # If y was a float like 15.7, the range is [x, 15.7], so the max int is 15.
    # However, the prompt implies x and y are likely integers. 
    # To be safe for the range [x, y], we check from floor(y) down to ceil(x).
    import math
    start = math.floor(y)
    end = math.ceil(x)
    
    for i in range(start, end - 1, -1):
        if i % 2 == 0:
            return i
            
    return -1
