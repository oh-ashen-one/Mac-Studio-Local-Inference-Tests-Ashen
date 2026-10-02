def tri(n):
    if n == 0:
        return [1]
    result = [0] * (n + 1)
    result[0] = 1
    result[1] = 3
    for i in range(2, n + 1):
        if i % 2 == 0:
            result[i] = 1 + i // 2
        else:
            result[i] = result[i - 1] + result[i - 2] + result[i + 1]
    return result
