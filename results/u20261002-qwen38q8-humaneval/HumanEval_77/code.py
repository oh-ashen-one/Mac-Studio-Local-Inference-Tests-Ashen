def iscube(a):
    if a < 0:
        a = -a
        sign = -1
    else:
        sign = 1
    
    # Find the integer cube root
    if a == 0:
        return True
    
    # Use round to get approximate cube root
    n = round(a ** (1/3))
    
    # Check nearby values due to floating point precision
    for candidate in [n - 1, n, n + 1]:
        if candidate < 0:
            continue
        if candidate ** 3 == a:
            return True
    
    return False
