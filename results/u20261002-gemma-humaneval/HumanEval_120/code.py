import heapq

def maximum(arr, k):
    """
    Given an array arr of integers and a positive integer k, return a sorted list 
    of length k with the maximum k numbers in arr.
    """
    if k == 0:
        return []
    
    # Use heapq.nlargest to get the k largest elements in O(n log k) time
    # Then sort them to return the result in ascending order
    largest_k = heapq.nlargest(k, arr)
    largest_k.sort()
    return largest_k
