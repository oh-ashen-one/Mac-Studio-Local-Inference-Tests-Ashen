def is_sorted(lst):
    if len(lst) != len(set(lst)):
        return False
    return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))
