def is_equal_to_sum_even(n):
    """Evaluate whether the given number n can be written as the sum of exactly 4 positive even numbers
    Example
    is_equal_to_sum_even(4) == False
    is_equal_to_sum_even(6) == False
    is_equal_to_sum_even(8) == True
    """
    # The smallest sum of 4 positive even numbers is 2 + 2 + 2 + 2 = 8.
    # Any sum of even numbers must be even.
    # If n is even and n >= 8, it can always be written as 2 + 2 + 2 + (n - 6).
    # Since n is even and n >= 8, (n - 6) is an even number >= 2.
    return n >= 8 and n % 2 == 0
