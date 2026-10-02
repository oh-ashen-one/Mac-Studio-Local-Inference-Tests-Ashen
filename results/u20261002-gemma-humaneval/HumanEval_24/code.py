import math

def largest_divisor(n: int) -> int:
    """ For a given number n, find the largest number that divides n evenly, smaller than n
    >>> largest_divisor(15)
    5
    """
    for i in range(int(math.sqrt(n)), 0, -1):
        if n % i == 0:
            # If i is a divisor, then n // i is also a divisor.
            # We want the largest divisor smaller than n.
            # The smallest divisor > 1 gives the largest divisor < n.
            # However, iterating downwards from sqrt(n) and checking n // i 
            # is a common way, but the simplest way for the largest is to 
            # find the smallest prime factor p, then n // p is the answer.
            pass
            
    # Optimized approach: find the smallest divisor > 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return n // i
    return 1
