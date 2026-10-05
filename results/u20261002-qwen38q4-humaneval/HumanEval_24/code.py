def largest_divisor(n: int) -> int:
    """ For a given number n, find the largest number that divides n evenly, smaller than n
    >>> largest_divisor(15)
    5
    """
    if n <= 1:
        raise ValueError("n must be greater than 1")
    
    # Find the smallest divisor greater than 1, then the largest proper divisor is n / smallest_divisor
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return n // i
    
    # If no divisor found, n is prime, so the largest proper divisor is 1
    return 1
