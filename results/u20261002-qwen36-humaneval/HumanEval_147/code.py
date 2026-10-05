def get_max_triples(n):
    """
    You are given a positive integer n. You have to create an integer array a of length n.
        For each i (1 ≤ i ≤ n), the value of a[i] = i * i - i + 1.
        Return the number of triples (a[i], a[j], a[k]) of a where i < j < k, 
    and a[i] + a[j] + a[k] is a multiple of 3.

    Example :
        Input: n = 5
        Output: 1
        Explanation: 
        a = [1, 3, 7, 13, 21]
        The only valid triple is (1, 7, 13).
    """
    # For each i (1-indexed), a[i] = i*i - i + 1
    # We need to count triples (i, j, k) with 1 <= i < j < k <= n
    # such that (a[i] + a[j] + a[k]) % 3 == 0
    
    # Let's analyze a[i] mod 3:
    # a[i] = i^2 - i + 1
    # Let's compute a[i] mod 3 for i mod 3:
    # If i ≡ 0 (mod 3): i = 3m, a[i] = 9m^2 - 3m + 1 ≡ 1 (mod 3)
    # If i ≡ 1 (mod 3): i = 3m+1, a[i] = (3m+1)^2 - (3m+1) + 1 = 9m^2 + 6m + 1 - 3m - 1 + 1 = 9m^2 + 3m + 1 ≡ 1 (mod 3)
    # If i ≡ 2 (mod 3): i = 3m+2, a[i] = (3m+2)^2 - (3m+2) + 1 = 9m^2 + 12m + 4 - 3m - 2 + 1 = 9m^2 + 9m + 3 ≡ 0 (mod 3)
    
    # So:
    # i ≡ 0 mod 3 → a[i] ≡ 1 mod 3
    # i ≡ 1 mod 3 → a[i] ≡ 1 mod 3
    # i ≡ 2 mod 3 → a[i] ≡ 0 mod 3
    
    # Let's count how many indices i (1 to n) have a[i] ≡ 0, 1, 2 mod 3.
    # From above, a[i] is either 0 or 1 mod 3, never 2.
    
    # Count:
    # c0 = number of i in [1, n] where i ≡ 2 mod 3 (a[i] ≡ 0)
    # c1 = number of i in [1, n] where i ≡ 0 or 1 mod 3 (a[i] ≡ 1)
    # c2 = 0 (no a[i] ≡ 2 mod 3)
    
    # We need triples (i,j,k) with i<j<k such that (a[i]+a[j]+a[k]) % 3 == 0.
    # The sum mod 3 can be:
    # 0+0+0 = 0 ✓
    # 0+0+1 = 1 ✗
    # 0+1+1 = 2 ✗
    # 1+1+1 = 3 ≡ 0 ✓
    
    # So valid triples are:
    # All three from c0 group: C(c0, 3)
    # All three from c1 group: C(c1, 3)
    
    # Let's compute c0 and c1.
    # c0 = number of i in [1, n] where i ≡ 2 mod 3
    # c1 = n - c0
    
    # Number of i in [1, n] with i ≡ 2 mod 3:
    # These are i = 2, 5, 8, ...
    # The largest such i ≤ n is: 2 + 3*(k-1) ≤ n → k-1 ≤ (n-2)/3 → k = floor((n-2)/3) + 1 if n >= 2, else 0
    
    # Let's compute c0 directly:
    # c0 = number of integers i in [1, n] such that i % 3 == 2
    
    c0 = 0
    for i in range(1, n + 1):
        if i % 3 == 2:
            c0 += 1
    c1 = n - c0
    
    # Count triples: C(c0, 3) + C(c1, 3)
    def comb3(x):
        if x < 3:
            return 0
        return x * (x - 1) * (x - 2) // 6
    
    return comb3(c0) + comb3(c1)
