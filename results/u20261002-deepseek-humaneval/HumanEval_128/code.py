def prod_signs(arr):
    if not arr:
        return None
    sign_product = 1
    magnitude_sum = 0
    for x in arr:
        if x > 0:
            sign_product *= 1
        elif x < 0:
            sign_product *= -1
        else:
            sign_product *= 0
        magnitude_sum += abs(x)
    return magnitude_sum * sign_product
