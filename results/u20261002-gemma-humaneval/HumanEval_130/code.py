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
    # The sequence is defined by:
    # tri(0) is not explicitly defined, but the example tri(3) = [1, 3, 2, 8] 
    # implies tri(0) = 1.
    # tri(1) = 3
    # tri(n) = 1 + n/2 if n is even
    # tri(n) = tri(n-1) + tri(n-2) + tri(n+1) if n is odd
    
    # To solve for tri(n) when n is odd, we need tri(n+1).
    # Since n+1 is even, tri(n+1) = 1 + (n+1)/2.
    # Thus for odd n: tri(n) = tri(n-1) + tri(n-2) + (1 + (n+1)/2)
    
    res = []
    for i in range(n + 1):
        if i == 0:
            res.append(1)
        elif i == 1:
            res.append(3)
        elif i % 2 == 0:
            res.append(int(1 + i / 2))
        else:
            # i is odd, i >= 3
            # tri(i) = tri(i-1) + tri(i-2) + tri(i+1)
            # tri(i+1) = 1 + (i+1)/2
            val = res[i-1] + res[i-2] + int(1 + (i + 1) / 2)
            res.append(val)
            
    return res
