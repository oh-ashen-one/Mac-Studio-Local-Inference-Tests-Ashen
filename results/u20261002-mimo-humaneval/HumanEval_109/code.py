def move_one_ball(arr):
    if not arr:
        return True
    n = len(arr)
    sorted_arr = sorted(arr)
    # Find the index of the minimum element in arr
    min_index = arr.index(min(arr))
    # Rotate arr so that the minimum element is at the beginning
    rotated = arr[min_index:] + arr[:min_index]
    return rotated == sorted_arr
