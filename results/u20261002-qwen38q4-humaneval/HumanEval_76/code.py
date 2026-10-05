def is_simple_power(x, n):
    """Your task is to write a function that returns true if a number x is a simple
    power of n and false in other cases.
    x is a simple power of n if n**int=x
    For example:
    is_simple_power(1, 4) => true
    is_simple_power(2, 2) => true
    is_simple_power(8, 2) => true
    is_simple_power(3, 2) => false
    is_simple_power(3, 1) => false
    is_simple_power(5, 3) => false
    """
    if n == 1:
        return x == 1
    if n == 0:
        return x == 1  # 0**0 is 1, 0**positive is 0, so only x==1 works for n=0? Actually 0**0=1, 0**1=0, etc.
    if x == 1:
        return True  # n**0 = 1 for any n != 0
    if x < 0:
        # Negative x: only possible if n is negative and exponent is odd
        if n < 0:
            # Check if x is a power of n with odd exponent
            # n**k = x where k is odd
            # Let's try exponents
            k = 1
            while abs(n) ** k <= abs(x):
                if n ** k == x:
                    return True
                k += 2  # only odd exponents give negative results for negative base
            return False
        else:
            return False
    # x > 0, n != 0, n != 1
    if n < 0:
        # n is negative, x is positive: exponent must be even
        k = 2
        while abs(n) ** k <= x:
            if n ** k == x:
                return True
            k += 2
        return False
    # n > 0, x > 0
    k = 1
    while n ** k <= x:
        if n ** k == x:
            return True
        k += 1
    return False
