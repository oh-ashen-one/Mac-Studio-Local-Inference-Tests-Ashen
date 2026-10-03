from itertools import combinations_with_replacement

def is_multiply_prime(a):
    """Write a function that returns true if the given number is the multiplication of 3 prime numbers
    and false otherwise.
    Knowing that (a) is less then 100. 
    Example:
    is_multiply_prime(30) == True
    30 = 2 * 3 * 5
    """
    if a < 8:
        return False

    # Generate primes less than 100
    primes = []
    for n in range(2, 100):
        is_prime = True
        for p in range(2, int(n**0.5) + 1):
            if n % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(n)

    # Check if 'a' can be formed by multiplying 3 primes (repetition allowed)
    for p1, p2, p3 in combinations_with_replacement(primes, 3):
        if p1 * p2 * p3 == a:
            return True

    return False
