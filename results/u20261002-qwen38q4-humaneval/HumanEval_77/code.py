def iscube(a):
    '''
    Write a function that takes an integer a and returns True 
    if this integer is a cube of some integer number.
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
    
    # Handle negative numbers
    if a < 0:
        # Check if -a is a perfect cube
        n = -a
        # Find the integer cube root
        # For negative a, we need an integer k such that k^3 = a, so k is negative
        # Let k = -m where m > 0, then (-m)^3 = -m^3 = a, so m^3 = -a = n
        # So we check if n is a perfect cube
        m = round(n ** (1/3))
        # Check m and nearby values due to floating point issues
        for candidate in (m - 1, m, m + 1):
            if candidate >= 0 and candidate ** 3 == n:
                return True
        return False
    else:
        # a > 0
        n = a
        m = round(n ** (1/3))
        for candidate in (m - 1, m, m + 1):
            if candidate >= 0 and candidate ** 3 == n:
                return True
        return False
