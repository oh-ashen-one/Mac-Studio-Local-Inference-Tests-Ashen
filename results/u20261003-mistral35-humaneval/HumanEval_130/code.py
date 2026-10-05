def tri(n):
    if n == 0:
        return [1]
    sequence = [0] * (n + 1)
    sequence[0] = 1
    if n >= 1:
        sequence[1] = 3
    for i in range(2, n + 1):
        if i % 2 == 0:
            sequence[i] = 1 + i // 2
        else:
            sequence[i] = sequence[i - 1] + sequence[i - 2] + (1 + (i + 1) // 2 if (i + 1) <= n else 1 + (i + 1) // 2)
    return sequence
