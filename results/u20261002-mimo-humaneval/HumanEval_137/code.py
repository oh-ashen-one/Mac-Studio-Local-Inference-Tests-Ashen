def compare_one(a, b):
    def to_float(x):
        if isinstance(x, str):
            return float(x.replace(',', '.'))
        return float(x)

    fa = to_float(a)
    fb = to_float(b)

    if fa == fb:
        return None
    return a if fa > fb else b
