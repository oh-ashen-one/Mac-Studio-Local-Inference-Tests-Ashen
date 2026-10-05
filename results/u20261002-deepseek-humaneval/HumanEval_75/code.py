import math

def is_multiply_prime(a):
    if a < 2:
        return False
    primes = []
    n = a
    for i in range(2, int(math.sqrt(a)) + 1):
        while n % i == 0:
            primes.append(i)
            n //= i
    if n > 1:
        primes.append(n)
    return len(primes) == 3
