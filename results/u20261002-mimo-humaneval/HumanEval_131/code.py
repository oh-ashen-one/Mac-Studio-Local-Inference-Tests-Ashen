def digits(n):
    """Given a positive integer n, return the product of the odd digits.
    Return 0 if all digits are even.
    For example:
    digits(1)  == 1
    digits(4)  == 0
    digits(235) == 15
    """
    product = 1
    found_odd = False
    for ch in str(n):
        d = int(ch)
        if d % 2 == 1:
            product *= d
            found_odd = True
    return product if found_odd else 0
