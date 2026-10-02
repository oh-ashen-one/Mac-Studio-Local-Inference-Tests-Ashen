def compare_one(a, b):
    """
    Create a function that takes integers, floats, or strings representing
    real numbers, and returns the larger variable in its given variable type.
    Return None if the values are equal.
    Note: If a real number is represented as a string, the floating point might be . or ,
    """
    def to_float(val):
        if isinstance(val, (int, float)):
            return float(val)
        # Replace comma with dot for float conversion
        return float(str(val).replace(',', '.'))

    val_a = to_float(a)
    val_b = to_float(b)

    if val_a > val_b:
        return a
    elif val_b > val_a:
        return b
    else:
        return None
