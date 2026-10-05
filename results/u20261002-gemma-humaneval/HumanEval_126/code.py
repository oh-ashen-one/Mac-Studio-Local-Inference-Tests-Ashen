from collections import Counter

def is_sorted(lst):
    '''
    Given a list of numbers, return whether or not they are sorted
    in ascending order. If list has more than 1 duplicate of the same
    number, return False. Assume no negative numbers and only integers.
    '''
    # Check if sorted in ascending order
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
            
    # Check if any number appears more than twice
    counts = Counter(lst)
    for count in counts.values():
        if count > 2:
            return False
            
    return True
