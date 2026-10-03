def tri(n):
    """Everyone knows Fibonacci sequence, it was studied deeply by mathematicians in 
    the last couple centuries. However, what people don't know is Tribonacci sequence.
    Tribonacci sequence is defined by the recurrence:
    tri(1) = 3
    tri(n) = 1 + n / 2, if n is even.
    tri(n) =  tri(n - 1) + tri(n - 2) + tri(n + 1), if n is odd.
    For example:
    tri(2) = 1 + (2 / 2) = 2
    tri(4) = 3
    tri(3) = tri(2) + tri(1) + tri(4)
           = 2 + 3 + 3 = 8 
    You are given a non-negative integer number n, you have to a return a list of the 
    first n + 1 numbers of the Tribonacci sequence.
    Examples:
    tri(3) = [1, 3, 2, 8]
    """
    if n < 0:
        return []
    
    # We need to compute tri(0) through tri(n)
    # tri(0) is not explicitly defined in the problem, but from the example:
    # tri(3) = [1, 3, 2, 8]
    # So tri(0) = 1, tri(1) = 3, tri(2) = 2, tri(3) = 8
    
    # Let's figure out the pattern:
    # For even n: tri(n) = 1 + n/2
    # tri(0) = 1 + 0/2 = 1 ✓
    # tri(2) = 1 + 2/2 = 2 ✓
    # tri(4) = 1 + 4/2 = 3 ✓
    
    # For odd n: tri(n) = tri(n-1) + tri(n-2) + tri(n+1)
    # tri(1) = 3 (given)
    # tri(3) = tri(2) + tri(1) + tri(4) = 2 + 3 + 3 = 8 ✓
    
    # So we can compute:
    # - Even indices directly: tri(n) = 1 + n/2
    # - Odd indices using the recurrence, but we need tri(n+1) which is even, so we can compute it
    
    # Let's build the list from 0 to n
    result = [0] * (n + 1)
    
    # Fill in even indices first
    for i in range(0, n + 1):
        if i % 2 == 0:
            result[i] = 1 + i / 2
    
    # Now fill in odd indices
    # For odd i: tri(i) = tri(i-1) + tri(i-2) + tri(i+1)
    # tri(i-1) is even, tri(i-2) is odd (if i-2 >= 1) or even (if i-2 == 0)
    # tri(i+1) is even
    
    # We need to be careful about the order. Let's think about this:
    # For i = 1: tri(1) = 3 (given, not from recurrence)
    # For i = 3: tri(3) = tri(2) + tri(1) + tri(4)
    # For i = 5: tri(5) = tri(4) + tri(3) + tri(6)
    
    # So for odd i >= 3, we need tri(i-2) which is odd and smaller, so we should compute in increasing order
    
    # Set tri(1) = 3
    if n >= 1:
        result[1] = 3
    
    # For odd i >= 3
    for i in range(3, n + 1, 2):
        # tri(i) = tri(i-1) + tri(i-2) + tri(i+1)
        # tri(i-1) is even, already computed
        # tri(i-2) is odd, already computed (since i-2 < i and we're going in increasing order)
        # tri(i+1) is even, already computed
        result[i] = result[i - 1] + result[i - 2] + result[i + 1]
    
    return result
