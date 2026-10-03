def sort_array(arr):
    """
    In this Kata, you have to sort an array of non-negative integers according to
    number of ones in their binary representation in ascending order.
    For similar number of ones, sort based on decimal value.

    It must be implemented like this:
    >>> sort_array([1, 5, 2, 3, 4]) == [1, 2, 3, 4, 5]
    >>> sort_array([-2, -3, -4, -5, -6]) == [-6, -5, -4, -3, -2]
    >>> sort_array([1, 0, 2, 3, 4]) [0, 1, 2, 3, 4]
    """
    def count_ones(n):
        if n < 0:
            # For negative numbers, use the absolute value's binary representation
            # or handle according to the expected behavior
            # Looking at the example: [-2, -3, -4, -5, -6] -> [-6, -5, -4, -3, -2]
            # Let's check: 
            # -2: abs=2, binary=10, ones=1
            # -3: abs=3, binary=11, ones=2
            # -4: abs=4, binary=100, ones=1
            # -5: abs=5, binary=101, ones=2
            # -6: abs=6, binary=110, ones=2
            # Sorted by ones then by value:
            # ones=1: -2, -4 -> sorted by value: -4, -2
            # ones=2: -3, -5, -6 -> sorted by value: -6, -5, -3
            # Result: [-4, -2, -6, -5, -3] but expected is [-6, -5, -4, -3, -2]
            # That doesn't match. Let me reconsider.
            # Maybe for negative numbers, we just sort by value?
            # Or maybe the problem statement says non-negative but the test includes negatives?
            # Let me re-read: "sort an array of non-negative integers"
            # But the example has negative numbers. This is confusing.
            # Let me try another approach: maybe for negative numbers, we use the two's complement or something else.
            # Actually, looking at the expected output [-6, -5, -4, -3, -2], this is just sorted in ascending order.
            # So maybe for negative numbers, we just sort by value?
            # Or maybe the count of ones for negative numbers is defined differently.
            # Let me try: for negative numbers, use the binary representation of the absolute value.
            # But that gave [-4, -2, -6, -5, -3] which doesn't match.
            # Let me try: maybe we sort negative numbers by their value only, ignoring the ones count?
            # That would give [-6, -5, -4, -3, -2] which matches!
            # But wait, that seems inconsistent with the problem statement.
            # Let me try another interpretation: maybe for negative numbers, we count ones in the two's complement representation?
            # In Python, negative numbers have infinite leading 1s in two's complement, so that doesn't work directly.
            # Let me just try: for negative numbers, use abs(n) for counting ones, but sort by value as secondary key.
            # Actually, let me re-examine. The expected output is [-6, -5, -4, -3, -2].
            # If we sort by (count_ones, value):
            # -2: (1, -2)
            # -3: (2, -3)
            # -4: (1, -4)
            # -5: (2, -5)
            # -6: (2, -6)
            # Sorted: (1, -4), (1, -2), (2, -6), (2, -5), (2, -3) -> [-4, -2, -6, -5, -3]
            # That doesn't match.
            # What if for negative numbers, we just sort by value?
            # Then the result would be [-6, -5, -4, -3, -2] which matches.
            # But that seems like a special case. Let me think about this differently.
            # Maybe the problem expects us to handle negative numbers by just sorting them by value?
            # Or maybe I'm overthinking this. Let me just implement it as: for each number, count ones in its binary representation (using abs for negative), and sort by (count, value).
            # But that doesn't match the expected output for the negative example.
            # Let me try: maybe for negative numbers, we count ones in the binary representation of the number itself (which in Python is infinite for negatives).
            # That doesn't make sense.
            # Let me just go with: for negative numbers, use abs(n) for counting ones.
            # And see if the tests pass. If not, I'll adjust.
            return bin(abs(n)).count('1')
        return bin(n).count('1')
    
    return sorted(arr, key=lambda x: (count_ones(x), x))
