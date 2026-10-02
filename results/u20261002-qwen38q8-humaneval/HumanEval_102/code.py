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
    
    # Find the largest even number in [x, y]
    # Start from y and go down to x
    # The largest even number <= y is:
    if y % 2 == 0:
        candidate = y
    else:
        candidate = y - 1
    
    if candidate >= x:
        return candidate
    else:
        return -1
