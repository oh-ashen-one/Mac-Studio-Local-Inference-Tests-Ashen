def double_the_difference(lst):
    total = 0
    for num in lst:
        if isinstance(num, int) and not isinstance(num, bool) and num > 0 and num % 2 != 0:
            total += num * num
    return total
