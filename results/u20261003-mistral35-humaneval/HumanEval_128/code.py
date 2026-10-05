from math import prod

def prod_signs(arr):
    if not arr:
        return None
    signs = [1 if x > 0 else -1 if x < 0 else 0 for x in arr]
    product_of_signs = prod(signs)
    sum_of_magnitudes = sum(abs(x) for x in arr)
    return sum_of_magnitudes * product_of_signs
