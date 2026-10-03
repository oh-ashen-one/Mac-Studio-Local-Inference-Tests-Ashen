def maximum(arr, k):
    """
    Given an array arr of integers and a positive integer k, return a sorted list 
    of length k with the maximum k numbers in arr.
    """
    if k == 0:
        return []
    # Get the k largest elements, then sort them
    largest_k = sorted(arr, reverse=True)[:k]
    return sorted(largest_k)
