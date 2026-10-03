def is_sorted(lst):
    if len(lst) <= 1:
        return True
    
    # Check if sorted in ascending order
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
    
    # Check for more than 1 duplicate of the same number
    # Count occurrences of each number
    counts = {}
    for num in lst:
        counts[num] = counts.get(num, 0) + 1
        if counts[num] > 2:
            return False
    
    return True
