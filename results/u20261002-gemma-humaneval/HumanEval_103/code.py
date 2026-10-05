import math

def rounded_avg(n, m):
    """You are given two positive integers n and m, and your task is to compute the
    average of the integers from n through m (including n and m). 
    Round the answer to the nearest integer and convert that to binary.
    If n is greater than m, return -1.
    Example:
    rounded_avg(1, 5) => "0b11"
    rounded_avg(7, 5) => -1
    rounded_avg(10, 20) => "0b1111"
    rounded_avg(20, 33) => "0b11010"
    """
    if n > m:
        return -1
    
    # The sum of integers from n to m is (n + m) * (m - n + 1) / 2
    # The count of integers is (m - n + 1)
    # Average = (n + m) / 2
    avg = (n + m) / 2
    
    # Round to nearest integer. 
    # Python's round() rounds to the nearest even number for .5 cases.
    # Standard mathematical rounding (round half up) is often expected in these challenges.
    # However, for (n+m)/2, the result is either .0 or .5.
    # Using int(avg + 0.5) implements round half up.
    rounded_val = int(avg + 0.5)
    
    return bin(rounded_val)
