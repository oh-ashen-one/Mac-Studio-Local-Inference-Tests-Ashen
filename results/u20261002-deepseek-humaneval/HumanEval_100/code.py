def make_a_pile(n):
    result = []
    current = n
    for i in range(n):
        result.append(current)
        if current % 2 == 0:
            current += 2
        else:
            current += 2
    return result
