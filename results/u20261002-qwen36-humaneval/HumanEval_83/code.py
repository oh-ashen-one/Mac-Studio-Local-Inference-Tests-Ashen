def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    if n == 1:
        # 1-digit numbers: 1 through 9. Those that start or end with 1: just 1.
        return 1
    
    # n-digit numbers range from 10^(n-1) to 10^n - 1
    # Count numbers that start with 1:
    #   First digit is 1, remaining n-1 digits can be anything (0-9)
    #   So 1 * 10^(n-1) numbers
    # Count numbers that end with 1:
    #   Last digit is 1, first digit can be 1-9 (9 choices), middle n-2 digits can be 0-9
    #   So 9 * 10^(n-2) numbers
    # But we double-counted numbers that both start AND end with 1:
    #   First digit is 1, last digit is 1, middle n-2 digits can be anything
    #   So 1 * 10^(n-2) numbers
    # By inclusion-exclusion: start_with_1 + end_with_1 - both
    # = 10^(n-1) + 9 * 10^(n-2) - 10^(n-2)
    # = 10^(n-1) + 8 * 10^(n-2)
    
    if n == 1:
        return 1
    
    start_with_1 = 10 ** (n - 1)
    end_with_1 = 9 * (10 ** (n - 2))
    both = 10 ** (n - 2)
    
    return start_with_1 + end_with_1 - both
