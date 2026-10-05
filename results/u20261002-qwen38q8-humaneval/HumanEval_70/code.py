def strange_sort_list(lst):
    if not lst:
        return []
    
    lst = sorted(lst)
    result = []
    left = 0
    right = len(lst) - 1
    take_min = True
    
    while left <= right:
        if take_min:
            result.append(lst[left])
            left += 1
        else:
            result.append(lst[right])
            right -= 1
        take_min = not take_min
    
    return result
