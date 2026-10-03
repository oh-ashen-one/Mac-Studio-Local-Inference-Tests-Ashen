```python
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
    
    # Base case: tri(1) = 3
    # tri(0) is not defined by the recurrence, but the example tri(3) = [1, 3, 2, 8]
    # implies tri(0) = 1.
    # We can deduce tri(0) from the odd recurrence if we assume it holds for n=1:
    # tri(1) = tri(0) + tri(-1) + tri(2)
    # 3 = tri(0) + tri(-1) + 2
    # tri(0) + tri(-1) = 1
    # If we assume tri(-1) = 0 (or similar), tri(0) = 1.
    # Given the example, we hardcode tri(0) = 1.
    
    if n == 0:
        return [1]
    
    # tri(1) = 3
    # tri(2) = 1 + 2/2 = 2
    # tri(3) = tri(2) + tri(1) + tri(4)
    # tri(4) = 1 + 4/2 = 3
    # tri(3) = 2 + 3 + 3 = 8
    
    # We need to compute up to n.
    # The recurrence for odd n depends on n+1.
    # So to compute tri(n) for odd n, we need tri(n+1).
    # tri(n+1) is even, so it's 1 + (n+1)/2.
    # So we can compute tri(n) for any odd n directly.
    
    # However, the sequence definition is a bit circular for odd numbers if we don't
    # have the even ones.
    # But even numbers are defined explicitly: tri(even) = 1 + even/2.
    # So we can fill the list for even indices easily.
    # For odd indices, we use the recurrence: tri(odd) = tri(odd-1) + tri(odd-2) + tri(odd+1).
    # tri(odd-1) is even (known).
    # tri(odd-2) is odd (needs to be computed).
    # tri(odd+1) is even (known).
    
    # So we can compute odd indices in increasing order.
    # tri(1) is given as 3.
    # tri(3) depends on tri(1) and tri(2), tri(4).
    # tri(5) depends on tri(3) and tri(4), tri(6).
    
    # Let's build the list.
    # We need to handle n up to n.
    # If n is even, we need to compute up to n.
    # If n is odd, we need to compute up to n.
    # The recurrence for tri(n) (odd) needs tri(n+1).
    # tri(n+1) is even, so it's 1 + (n+1)/2.
    
    # So we can compute tri(n) for any odd n without needing the full list up to n+1
    # if we just calculate tri(n+1) on the fly.
    
    # But the problem asks for a list of first n+1 numbers.
    # So we need to fill indices 0 to n.
    
    # Let's initialize the list.
    # tri(0) = 1
    # tri(1) = 3
    # tri(2) = 2
    
    # We can iterate from 0 to n.
    # If i is even: tri(i) = 1 + i/2
    # If i is odd:
    #   if i == 1: tri(1) = 3
    #   else: tri(i) = tri(i-1) + tri(i-2) + tri(i+1)
    #   Note: tri(i+1) is even, so tri(i+1) = 1 + (i+1)/2.
    #   tri(i-1) is even, so tri(i-1) = 1 + (i-1)/2.
    #   tri(i-2) is odd, so it should be already computed if we iterate in order.
    
    # Wait, tri(i-1) is even, so it's 1 + (i-1)/2.
    # tri(i+1) is even, so it's 1 + (i+1)/2.
    # So tri(i) = (1 + (i-1)/2) + tri(i-2) + (1 + (i+1)/2)
    # tri(i) = 2 + (i-1)/2 + (i+1)/2 + tri(i-2)
    # tri(i) = 2 + i - 0.5 + 0.5 + tri(i-2)  (Wait, (i-1)/2 + (i+1)/2 = (2i)/2 = i)
    # tri(i) = 2 + i + tri(i-2)
    
    # Let's check for i=3:
    # tri(3) = 2 + 3 + tri(1) = 5 + 3 = 8. Correct.
    
    # Let's check for i=1:
    # tri(1) = 2 + 1 + tri(-1) = 3 + tri(-1).
    # We know tri(1) = 3, so tri(-1) = 0.
    # This matches our assumption.
    
    # So the recurrence for odd i >= 1 is:
    # tri(i) = i + 2 + tri(i-2)
    
    # This is much simpler!
    # We don't even need to check if i is even or odd for the calculation if we just
    # use the formula for even and the recurrence for odd.
    
    # Let's verify even formula:
    # tri(even) = 1 + even/2.
    
    # So we can just iterate.
    
    result = []
    # We need to handle n=0, n=1, n=2...
    
    # tri(0) = 1
    # tri(1) = 3
    # tri(2) = 2
    
    # Let's just fill the list.
    # We need to be careful with indices.
    
    # If n is 0, return [1].
    # If n is 1, return [1, 3].
    # If n is 2, return [1, 3, 2].
    
    # Let's create a list of size n+1.
    # Initialize with 0s.
    seq = [0] * (n + 1)
    
    if n >= 0:
        seq[0] = 1
    if n >= 1:
        seq[1] = 3
    if n >= 2:
        seq[2] = 2
    
    # Now iterate from 3 to n.
    for i in range(3, n + 1):
        if i % 2 == 0:
            # Even
            seq[i] = 1 + i / 2
        else:
            # Odd
            # tri(i) = tri(i-1) + tri(i-2) + tri(i+1)
            # tri(i-1) is even, so 1 + (i-1)/2
            # tri(i+1) is even, so 1 + (i+1)/2
            # tri(i-2) is in seq[i-2]
            
            # Wait, if i is odd, i+1 is even.
            # We don't have seq[i+1] yet if we are iterating up to n.
            # But we know the formula for even numbers.
            # So we can calculate tri(i+1) on the fly.
            
            tri_i_minus_1 = 1 + (i - 1) / 2
            tri_i_plus_1 = 1 + (i + 1) / 2
            tri_i_minus_2 = seq[i - 2]
            
            seq[i] = tri_i_minus_1 + tri_i_minus_2 + tri_i_plus_1
    
    # The problem asks for a list of the first n+1 numbers.
   