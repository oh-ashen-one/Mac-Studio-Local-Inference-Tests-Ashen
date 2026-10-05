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
        # For negative numbers, we need to handle them specially.
        # The problem says "non-negative integers" but the example includes negatives.
        # Let's count the number of 1 bits in the binary representation.
        # For negative numbers, Python's bin() gives a negative sign with positive bits.
        # We need to think about what "number of ones in their binary representation" means for negatives.
        # Looking at the example: sort_array([-2, -3, -4, -5, -6]) == [-6, -5, -4, -3, -2]
        # -2 in binary (two's complement, let's say 8-bit): 11111110 -> 7 ones
        # -3: 11111101 -> 7 ones
        # -4: 11111100 -> 6 ones
        # -5: 11111011 -> 6 ones
        # -6: 11111010 -> 5 ones
        # So sorting by number of ones ascending:
        # -6: 5 ones, -5: 6 ones, -4: 6 ones, -3: 7 ones, -2: 7 ones
        # For same number of ones, sort by decimal value ascending:
        # -6 (5 ones), then -5 and -4 (6 ones each): -5 < -4, so -5, -4, then -3 and -2 (7 ones each): -3 < -2
        # Result: [-6, -5, -4, -3, -2] which matches.
        # So for negative numbers, we count the number of 1 bits in their two's complement representation.
        # But how many bits? The problem doesn't specify. Let's use a fixed width, say 32 or 64 bits.
        # Actually, let's think differently. For negative numbers, we can use the number of 1 bits in the two's complement form.
        # In Python, we can simulate this by using a fixed number of bits, e.g., 32 bits.
        if n >= 0:
            return bin(n).count('1')
        else:
            # For negative numbers, use two's complement with 32 bits
            # Mask to 32 bits
            masked = n & 0xFFFFFFFF
            return bin(masked).count('1')
    
    return sorted(arr, key=lambda x: (count_ones(x), x))
