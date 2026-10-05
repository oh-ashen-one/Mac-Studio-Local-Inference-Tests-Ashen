def cycpattern_check(a, b):
    if len(b) == 0:
        return True
    combined = b + b
    for i in range(len(b)):
        rotation = combined[i:i+len(b)]
        if rotation in a:
            return True
    return False
