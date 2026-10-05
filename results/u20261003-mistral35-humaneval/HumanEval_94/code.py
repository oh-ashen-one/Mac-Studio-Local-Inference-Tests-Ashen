import math

def skjkasdkd(lst):
    def is_prime(n):
        if n <= 1:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

    primes = [x for x in lst if is_prime(x)]
    if not primes:
        return 0
    largest_prime = max(primes)
    return sum(int(d) for d in str(abs(largest_prime)))
