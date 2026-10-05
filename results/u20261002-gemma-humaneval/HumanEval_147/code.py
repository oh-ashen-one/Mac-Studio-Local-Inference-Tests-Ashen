def get_max_triples(n):
    """
    You are given a positive integer n. You have to create an integer array a of length n.
        For each i (1 ≤ i ≤ n), the value of a[i] = i * i - i + 1.
        Return the number of triples (a[i], a[j], a[k]) of a where i < j < k, 
    and a[i] + a[j] + a[k] is a multiple of 3.
    """
    # The sequence is a[i] = i^2 - i + 1 for i = 1 to n.
    # We need to find the number of triples (a[i], a[j], a[k]) such that 
    # (a[i] + a[j] + a[k]) % 3 == 0.
    # Let's analyze a[i] % 3:
    # i = 1: 1^2 - 1 + 1 = 1 -> 1 % 3 = 1
    # i = 2: 2^2 - 2 + 1 = 3 -> 3 % 3 = 0
    # i = 3: 3^2 - 3 + 1 = 7 -> 7 % 3 = 1
    # i = 4: 4^2 - 4 + 1 = 13 -> 13 % 3 = 1
    # i = 5: 5^2 - 5 + 1 = 21 -> 21 % 3 = 0
    # i = 6: 6^2 - 6 + 1 = 31 -> 31 % 3 = 1
    # Pattern of a[i] % 3: 1, 0, 1, 1, 0, 1, ...
    # a[i] % 3 is 0 if i % 3 == 2, and 1 if i % 3 == 1 or 0.
    
    # Count how many elements have remainder 0 and how many have remainder 1.
    # Remainder 0 occurs when i = 2, 5, 8... (i = 3k + 2)
    # Remainder 1 occurs when i = 1, 3, 4, 6, 7, 9...
    
    # Count of i in [1, n] such that i % 3 == 2:
    # These are 2, 5, ..., 3k+2 <= n => 3k <= n-2 => k <= (n-2)//3
    # Number of elements is ((n-2)//3) + 1 if n >= 2 else 0.
    count0 = (n + 1) // 3 if n >= 2 else 0
    # Wait, let's re-verify:
    # n=1: count0=0
    # n=2: count0=1 (i=2)
    # n=3: count0=1 (i=2)
    # n=4: count0=1 (i=2)
    # n=5: count0=2 (i=2, 5)
    # Correct formula for count of i in [1, n] where i % 3 == 2 is (n + 1) // 3.
    # Let's check: n=1: 2//3=0; n=2: 3//3=1; n=3: 4//3=1; n=4: 5//3=1; n=5: 6//3=2. Correct.
    
    c0 = (n + 1) // 3
    c1 = n - c0
    
    # We need (r_i + r_j + r_k) % 3 == 0 where r is the remainder.
    # Possible combinations of (r_i, r_j, r_k) from {0, 1}:
    # 1. (0, 0, 0): 0+0+0 = 0 (multiple of 3)
    # 2. (1, 1, 1): 1+1+1 = 3 (multiple of 3)
    # 3. (0, 0, 1): 0+0+1 = 1 (no)
    # 4. (0, 1, 1): 0+1+1 = 2 (no)
    
    # Number of ways to choose 3 from c0: c0 * (c0 - 1) * (c0 - 2) // 6
    # Number of ways to choose 3 from c1: c1 * (c1 - 1) * (c1 - 2) // 6
    
    ans = 0
    if c0 >= 3:
        ans += (c0 * (c0 - 1) * (c0 - 2)) // 6
    if c1 >= 3:
        ans += (c1 * (c1 - 1) * (c1 - 2)) // 6
        
    return ans
