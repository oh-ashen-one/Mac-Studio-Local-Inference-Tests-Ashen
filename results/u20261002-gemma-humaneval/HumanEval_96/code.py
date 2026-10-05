def count_up_to(n):
    """Implement a function that takes an non-negative integer and returns an array of the first n
    integers that are prime numbers and less than n.
    """
    if n < 2:
        return []
    
    primes = []
    for candidate in range(2, n):
        is_prime = True
        for i in range(2, int(candidate**0.5) + 1):
            if candidate % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
            
    return primes
