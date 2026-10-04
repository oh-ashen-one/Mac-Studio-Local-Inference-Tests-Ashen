import math

def is_multiply_prime(a):
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    prime_factors = []
    temp = a
    for i in range(2, temp + 1):
        while temp % i == 0 and is_prime(i):
            prime_factors.append(i)
            temp = temp // i
            if len(prime_factors) > 3:
                return False
    return len(prime_factors) == 3 and math.prod(prime_factors) == a
