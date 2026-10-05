import math

def is_simple_power(x, n):
    if n == 1:
        return x == 1
    if x == 1:
        return n == 1
    if n == 0:
        return False
    if x == 0:
        return False
    k = math.log(abs(x), abs(n))
    return abs(k - round(k)) < 1e-10 and n ** round(k) == x
