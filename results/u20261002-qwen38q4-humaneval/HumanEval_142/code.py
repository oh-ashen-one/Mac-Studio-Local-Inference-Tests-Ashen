def sum_squares(lst):
    total = 0
    for i, val in enumerate(lst):
        if i % 3 == 0:
            total += val * val
        elif i % 4 == 0:
            total += val * val * val
        else:
            total += val
    return total
