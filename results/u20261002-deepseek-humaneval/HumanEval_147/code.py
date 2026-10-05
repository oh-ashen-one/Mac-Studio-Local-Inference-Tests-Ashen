def get_max_triples(n):
    from collections import Counter
    a = [i * i - i + 1 for i in range(1, n + 1)]
    mods = [x % 3 for x in a]
    cnt = Counter(mods)
    total = 0
    # all three same mod
    for m in range(3):
        c = cnt[m]
        total += c * (c - 1) * (c - 2) // 6
    # one from each mod
    total += cnt[0] * cnt[1] * cnt[2]
    return total
