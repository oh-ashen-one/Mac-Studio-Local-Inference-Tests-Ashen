import math

def f(n):
    result = []
    for i in range(1, n + 1):
        if i % 2 == 0:
            result.append(math.factorial(i))
        else:
            result.append(i * (i + 1) // 2)
    return result
