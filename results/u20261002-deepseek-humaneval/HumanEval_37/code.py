def sort_even(l: list):
    even_values = sorted(l[0::2])
    result = list(l)
    result[0::2] = even_values
    return result
