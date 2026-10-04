def fib(n: int) -> int:
    """Return n-th Fibonacci number.
    >>> fib(10)
    55
    >>> fib(1)
    1
    >>> fib(8)
    21
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
