import math

def prime_fib(n: int):
    def is_prime(num):
        if num < 2:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(math.isqrt(num)) + 1, 2):
            if num % i == 0:
                return False
        return True

    count = 0
    a, b = 1, 1
    while True:
        if a > 1 and is_prime(a):
            count += 1
            if count == n:
                return a
        a, b = b, a + b
