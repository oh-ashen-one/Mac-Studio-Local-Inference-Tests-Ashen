def cycpattern_check(a, b):
    if not b:
        return True
    n = len(b)
    for i in range(n):
        rotated = b[i:] + b[:i]
        if rotated in a:
            return True
    return False
