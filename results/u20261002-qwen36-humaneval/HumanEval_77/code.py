def iscube(a):
    '''
    Write a function that takes an integer a and returns True 
    if this ingeger is a cube of some integer number.
    Note: you may assume the input is always valid.
    Examples:
    iscube(1) ==> True
    iscube(2) ==> False
    iscube(-1) ==> True
    iscube(64) ==> True
    iscube(0) ==> True
    iscube(180) ==> False
    '''
    if a == 0:
        return True
    
    # Find the cube root
    # For negative numbers, cube root is negative
    if a < 0:
        # Take absolute value, find cube root, then check
        abs_a = -a
        # Find integer cube root
        c = round(abs_a ** (1/3))
        # Check c^3 == abs_a
        if c ** 3 == abs_a:
            return True
        # Also check c-1 and c+1 due to floating point inaccuracies
        if (c - 1) ** 3 == abs_a:
            return True
        if (c + 1) ** 3 == abs_a:
            return True
        return False
    else:
        c = round(a ** (1/3))
        if c ** 3 == a:
            return True
        if (c - 1) ** 3 == a:
            return True
        if (c + 1) ** 3 == a:
            return True
        return False
