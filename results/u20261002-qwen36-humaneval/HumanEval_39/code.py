def prime_fib(n: int):
    """
    prime_fib returns n-th number that is a Fibonacci number and it's also prime.
    >>> prime_fib(1)
    2
    >>> prime_fib(2)
    3
    >>> prime_fib(3)
    5
    >>> prime_fib(4)
    13
    >>> prime_fib(5)
    89
    """
    def is_prime(num):
        if num < 2:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(num**0.5) + 1, 2):
            if num % i == 0:
                return False
        return True
    
    # Generate Fibonacci numbers and check which ones are prime
    # Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...
    # Prime Fibonacci numbers: 2, 3, 5, 13, 89, ...
    
    count = 0
    a, b = 0, 1
    
    while True:
        fib = a
        if is_prime(fib):
            count += 1
            if count == n:
                return fib
        a, b = b, a + b
