def is_equal_to_sum_even(n):
    """Evaluate whether the given number n can be written as the sum of exactly 4 positive even numbers
    Example
    is_equal_to_sum_even(4) == False
    is_equal_to_sum_even(6) == False
    is_equal_to_sum_even(8) == True
    """
    # The smallest sum of 4 positive even numbers is 2+2+2+2 = 8
    # Any even number >= 8 can be written as the sum of 4 positive even numbers
    # For example, n = 8: 2+2+2+2
    # n = 10: 2+2+2+4
    # n = 12: 2+2+4+4 or 2+2+2+6
    # In general, for any even n >= 8, we can write n = 2 + 2 + 2 + (n-6)
    # where n-6 is even and >= 2 (since n >= 8)
    # For odd numbers, it's impossible since sum of even numbers is always even
    if n < 8:
        return False
    return n % 2 == 0
