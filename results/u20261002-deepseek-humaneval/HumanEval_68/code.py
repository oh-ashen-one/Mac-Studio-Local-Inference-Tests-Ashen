def pluck(arr):
    best_value = None
    best_index = None
    for i, value in enumerate(arr):
        if value % 2 == 0:
            if best_value is None or value < best_value:
                best_value = value
                best_index = i
    if best_value is None:
        return []
    return [best_value, best_index]
