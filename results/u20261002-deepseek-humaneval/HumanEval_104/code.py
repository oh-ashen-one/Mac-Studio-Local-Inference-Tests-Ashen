def unique_digits(x):
    result = []
    for num in x:
        if all(int(d) % 2 != 0 for d in str(num)):
            result.append(num)
    return sorted(result)
