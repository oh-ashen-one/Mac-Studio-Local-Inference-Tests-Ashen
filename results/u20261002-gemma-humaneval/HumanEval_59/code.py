import math

def largest_prime_factor(n: int):
    """Return the largest prime factor of n. Assume n > 1 and is not a prime.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            temp //= d
        else:
            d += 1
    return temp if temp > 1 else d
