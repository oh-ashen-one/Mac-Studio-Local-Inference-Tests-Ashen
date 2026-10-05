def move_one_ball(arr):
    if not arr:
        return True
    n = len(arr)
    sorted_arr = sorted(arr)
    for shift in range(n):
        shifted = arr[-shift:] + arr[:-shift]
        if shifted == sorted_arr:
            return True
    return False
