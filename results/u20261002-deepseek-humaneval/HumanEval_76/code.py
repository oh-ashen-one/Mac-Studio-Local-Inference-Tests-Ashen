def is_simple_power(x, n):
    if n == 1:
        return x == 1
    if x == 1:
        return True
    power = 0
    result = 1
    while result < x:
        result *= n
        power += 1
    return result == x
