from typing import List

def minSubArraySum(nums: List[int]) -> int:
    """
    Given an array of integers nums, find the minimum sum of any non-empty sub-array
    of nums.
    Example
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
    # Kadane's algorithm modified for minimum sum
    min_so_far = nums[0]
    current_min = nums[0]
    
    for i in range(1, len(nums)):
        # Either start a new subarray at the current element or extend the existing one
        current_min = min(nums[i], current_min + nums[i])
        min_so_far = min(min_so_far, current_min)
        
    return min_so_far
