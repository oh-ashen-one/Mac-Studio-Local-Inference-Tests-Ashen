def is_simple_power(x, n):
    """Your task is to write a function that returns true if a number x is a simple
    power of n and false in other cases.
    x is a simple power of n if n**int=x
    """
    if x < 1:
        return False
    if x == 1:
        return True
    if n <= 1:
        return x == n
    
    current = n
    while current <= x:
        if current == x:
            return True
        current *= n
    return False
