def pluck(arr):
    """
    Given an array representing a branch of a tree that has non-negative integer nodes
    your task is to pluck one of the nodes and return it.
    The plucked node should be the node with the smallest even value.
    If multiple nodes with the same smallest even value are found return the node that has smallest index.

    The plucked node should be returned in a list, [ smalest_value, its index ],
    If there are no even values or the given array is empty, return [].
    """
    if not arr:
        return []

    smallest_even = float('inf')
    smallest_index = -1

    for i, val in enumerate(arr):
        if val % 2 == 0:
            if val < smallest_even:
                smallest_even = val
                smallest_index = i
    
    if smallest_index == -1:
        return []
    
    return [smallest_even, smallest_index]
