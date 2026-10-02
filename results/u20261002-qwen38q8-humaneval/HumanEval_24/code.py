def largest_divisor(n: int) -> int:
    """ For a given number n, find the largest number that divides n evenly, smaller than n
    >>> largest_divisor(15)
    5
    """
    if n <= 1:
        raise ValueError("n must be greater than 1")
    
    # Find the smallest divisor greater than 1, then n / that divisor is the largest proper divisor
    i = 2
    while i * i <= n:
        if n % i == 0:
            return n // i
        i += 1
    
    # If no divisor found, n is prime, so the largest proper divisor is 1
    return 1
