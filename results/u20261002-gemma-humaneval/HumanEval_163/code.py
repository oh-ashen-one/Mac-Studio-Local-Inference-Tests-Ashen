def generate_integers(a, b):
    """
    Given two positive integers a and b, return the even digits between a
    and b, in ascending order.

    For example:
    generate_integers(2, 8) => [2, 4, 6, 8]
    generate_integers(8, 2) => [2, 4, 6, 8]
    generate_integers(10, 14) => []
    """
    start = min(a, b)
    end = max(a, b)
    
    # The problem specifies "even digits", which are 0, 2, 4, 6, 8.
    # Since a and b are positive integers, we check for digits in the range [start, end].
    result = []
    for i in range(start, end + 1):
        if 0 <= i <= 9 and i % 2 == 0:
            result.append(i)
            
    return result
