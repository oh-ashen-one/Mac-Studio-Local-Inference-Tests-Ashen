def generate_integers(a, b):
    start = min(a, b)
    end = max(a, b)
    return [x for x in range(start, end + 1) if x % 2 == 0]
