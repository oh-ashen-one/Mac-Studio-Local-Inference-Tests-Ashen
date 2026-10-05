import math

def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    if n <= 0:
        return 0
    
    if n == 1:
        # Only the number 1 fits the criteria
        return 1
    
    # Total n-digit numbers = 9 * 10**(n-1)
    # Numbers starting with 1: 1 * 10**(n-1)
    # Numbers ending with 1: 9 * 10**(n-2)
    # Numbers starting AND ending with 1: 1 * 10**(n-2)
    
    # Using Inclusion-Exclusion Principle: |A or B| = |A| + |B| - |A and B|
    starts_with_1 = 10**(n - 1)
    ends_with_1 = 9 * (10**(n - 2))
    both = 10**(n - 2)
    
    return starts_with_1 + ends_with_1 - both
