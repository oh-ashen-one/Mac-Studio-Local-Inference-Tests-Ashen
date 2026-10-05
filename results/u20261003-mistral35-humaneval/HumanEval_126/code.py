from collections import Counter

def is_sorted(lst):
    if len(lst) == 0:
        return True
    # Check for more than one duplicate of any number
    counts = Counter(lst)
    if any(count > 2 for count in counts.values()):
        return False
    # Check if the list is sorted in ascending order
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
    return True
