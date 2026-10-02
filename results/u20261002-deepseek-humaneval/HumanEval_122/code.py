def add_elements(arr, k):
    return sum(x for x in arr[:k] if -99 <= x <= 99 or -9 <= x <= 9 or (x >= -99 and x <= 99))
