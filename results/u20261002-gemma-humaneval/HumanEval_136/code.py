from typing import List, Tuple, Optional

def largest_smallest_integers(lst: List[int]) -> Tuple[Optional[int], Optional[int]]:
    '''
    Create a function that returns a tuple (a, b), where 'a' is
    the largest of negative integers, and 'b' is the smallest
    of positive integers in a list.
    If there is no negative or positive integers, return them as None.
    '''
    negatives = [x for x in lst if x < 0]
    positives = [x for x in lst if x > 0]
    
    a = max(negatives) if negatives else None
    b = min(positives) if positives else None
    
    return (a, b)
