def get_max_triples(n):
    """
    You are given a positive integer n. You have to create an integer array a of length n.
        For each i (1 ≤ i ≤ n), the value of a[i] = i * i - i + 1.
        Return the number of triples (a[i], a[j], a[k]) of a where i < j < k, 
    and a[i] + a[j] + a[k] is a multiple of 3.
    """
    # a[i] = i^2 - i + 1
    # We only care about a[i] % 3.
    # i^2 - i + 1 = i(i-1) + 1.
    # i(i-1) is the product of two consecutive integers, so it is always even.
    # Let's check i(i-1) % 3:
    # If i % 3 == 0, i(i-1) % 3 == 0.
    # If i % 3 == 1, i(i-1) % 3 == 1*0 == 0.
    # If i % 3 == 2, i(i-1) % 3 == 2*1 == 2.
    # So i(i-1) % 3 is 0 if i % 3 != 2, and 2 if i % 3 == 2.
    # Then a[i] % 3 = (i(i-1) + 1) % 3.
    # If i % 3 != 2, a[i] % 3 = (0 + 1) % 3 = 1.
    # If i % 3 == 2, a[i] % 3 = (2 + 1) % 3 = 0.
    
    # So a[i] % 3 is 1 if i % 3 is 0 or 1.
    # a[i] % 3 is 0 if i % 3 is 2.
    
    # We need to count triples (i, j, k) with i < j < k such that
    # (a[i] + a[j] + a[k]) % 3 == 0.
    
    # Let's count how many indices i (1 <= i <= n) have i % 3 == 0, 1, 2.
    # Let c0 = count of i where i % 3 == 0
    # Let c1 = count of i where i % 3 == 1
    # Let c2 = count of i where i % 3 == 2
    
    # For a[i] % 3:
    # If i % 3 == 0 -> a[i] % 3 == 1
    # If i % 3 == 1 -> a[i] % 3 == 1
    # If i % 3 == 2 -> a[i] % 3 == 0
    
    # So we have:
    # count of a[i] % 3 == 1 is c0 + c1
    # count of a[i] % 3 == 0 is c2
    # count of a[i] % 3 == 2 is 0
    
    # We need sum of three elements to be divisible by 3.
    # Possible combinations of remainders (r1, r2, r3) where r1+r2+r3 % 3 == 0:
    # (0, 0, 0)
    # (1, 1, 1)
    # (0, 1, 2) - but we have no elements with remainder 2.
    
    # So we only need to count:
    # 1. Triples where all three have remainder 0.
    # 2. Triples where all three have remainder 1.
    
    # Let n0 = c2 (count of remainder 0)
    # Let n1 = c0 + c1 (count of remainder 1)
    
    # Number of triples with all remainder 0: C(n0, 3)
    # Number of triples with all remainder 1: C(n1, 3)
    
    # Calculate c0, c1, c2 for i in 1..n
    c0 = n // 3
    c1 = (n + 2) // 3 - (n + 1) // 3
    # Actually simpler:
    # i = 1, 2, 3, ..., n
    # i % 3 == 1: 1, 4, 7, ... count = (n + 2) // 3
    # i % 3 == 2: 2, 5, 8, ... count = (n + 1) // 3
    # i % 3 == 0: 3, 6, 9, ... count = n // 3
    
    c1 = (n + 2) // 3
    c2 = (n + 1) // 3
    c0 = n // 3
    
    n0 = c2
    n1 = c0 + c1
    
    def comb3(x):
        if x < 3:
            return 0
        return x * (x - 1) * (x - 2) // 6
    
    return comb3(n0) + comb3(n1)
