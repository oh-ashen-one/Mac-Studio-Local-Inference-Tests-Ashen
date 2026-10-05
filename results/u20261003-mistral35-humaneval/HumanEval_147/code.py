from collections import defaultdict

def get_max_triples(n):
    a = [i * i - i + 1 for i in range(1, n + 1)]
    mod_counts = defaultdict(int)
    for num in a:
        mod_counts[num % 3] += 1

    count = 0
    # Case 1: All three numbers are divisible by 3 (0 mod 3)
    count += mod_counts[0] * (mod_counts[0] - 1) * (mod_counts[0] - 2) // 6
    # Case 2: All three numbers are 1 mod 3
    count += mod_counts[1] * (mod_counts[1] - 1) * (mod_counts[1] - 2) // 6
    # Case 3: All three numbers are 2 mod 3
    count += mod_counts[2] * (mod_counts[2] - 1) * (mod_counts[2] - 2) // 6
    # Case 4: One from each mod (0, 1, 2)
    count += mod_counts[0] * mod_counts[1] * mod_counts[2]

    return count
