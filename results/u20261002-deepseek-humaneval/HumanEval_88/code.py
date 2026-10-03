def sort_array(array):
    if not array:
        return []
    if len(array) == 1:
        return array.copy()
    first = array[0]
    last = array[-1]
    if (first + last) % 2 == 1:
        return sorted(array)
    else:
        return sorted(array, reverse=True)
