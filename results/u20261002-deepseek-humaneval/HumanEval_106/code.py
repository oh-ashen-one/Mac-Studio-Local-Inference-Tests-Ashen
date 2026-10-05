def f(n):
    result = []
    for i in range(1, n + 1):
        if i % 2 == 0:
            # sum of numbers from 1 to i
            result.append(i * (i + 1) // 2)
        else:
            # factorial of i
            fact = 1
            for j in range(1, i + 1):
                fact *= j
            result.append(fact)
    return result
