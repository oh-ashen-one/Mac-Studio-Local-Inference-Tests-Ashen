import ast as _bench_ast
import operator as _bench_operator
def _bench_arithmetic_node(n):
    if isinstance(n, _bench_ast.Constant) and type(n.value) in (int, float): return n.value
    if isinstance(n, _bench_ast.UnaryOp) and isinstance(n.op, (_bench_ast.UAdd, _bench_ast.USub)):
        v = _bench_arithmetic_node(n.operand)
        return v if isinstance(n.op, _bench_ast.UAdd) else -v
    ops = {_bench_ast.Add: _bench_operator.add, _bench_ast.Sub: _bench_operator.sub, _bench_ast.Mult: _bench_operator.mul, _bench_ast.Div: _bench_operator.truediv, _bench_ast.FloorDiv: _bench_operator.floordiv, _bench_ast.Mod: _bench_operator.mod, _bench_ast.Pow: _bench_operator.pow}
    if isinstance(n, _bench_ast.BinOp) and type(n.op) in ops:
        return ops[type(n.op)](_bench_arithmetic_node(n.left), _bench_arithmetic_node(n.right))
    raise ValueError('Only numeric arithmetic is permitted by benchmark eval')
def eval(expression):
    return _bench_arithmetic_node(_bench_ast.parse(expression, mode='eval').body)


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
            # Looking at the example: sort_array([-2, -3, -4, -5, -6]) == [-6, -5, -4, -3, -2]
            # Let's check the number of ones in binary for these:
            # -2: in two's complement (assuming 32-bit), but let's think differently
            # Actually, for negative numbers, we might need to consider their absolute value
            # or the problem might expect us to handle them specially
            # Let's check: if we use abs(n) and count ones:
            # -2 -> 2 -> 10 -> 1 one
            # -3 -> 3 -> 11 -> 2 ones
            # -4 -> 4 -> 100 -> 1 one
            # -5 -> 5 -> 101 -> 2 ones
            # -6 -> 6 -> 110 -> 2 ones
            # Sorting by (count_ones, value):
            # (-2, 1), (-4, 1), (-3, 2), (-5, 2), (-6, 2)
            # After sorting: -2, -4, -3, -5, -6
            # But expected is [-6, -5, -4, -3, -2]
            # So that doesn't match. Let me reconsider.
            # Maybe for negative numbers, we should sort by the number of ones in their binary representation
            # using Python's bin() which gives '-0b...' for negatives
            # Let's check what bin() gives:
            # bin(-2) = '-0b10'
            # bin(-3) = '-0b11'
            # bin(-4) = '-0b100'
            # bin(-5) = '-0b101'
            # bin(-6) = '-0b110'
            # If we count ones in the string after removing '-0b':
            # -2: '10' -> 1
            # -3: '11' -> 2
            # -4: '100' -> 1
            # -5: '101' -> 2
            # -6: '110' -> 2
            # Same as before.
            # The expected output is [-6, -5, -4, -3, -2]
            # This is just ascending order by value.
            # Let me re-read the problem. It says "non-negative integers" but the example has negatives.
            # Perhaps for negative numbers, the sorting is just by value?
            # Or perhaps the number of ones is counted differently.
            # Let me try: maybe we should use the two's complement representation?
            # For a fixed bit width, say 8 bits:
            # -2: 11111110 -> 7 ones
            # -3: 11111101 -> 6 ones
            # -4: 11111100 -> 6 ones
            # -5: 11111011 -> 6 ones
            # -6: 11111010 -> 6 ones
            # Sorting by (count_ones, value):
            # (-3, 6), (-4, 6), (-5, 6), (-6, 6), (-2, 7)
            # After sorting: -3, -4, -5, -6, -2
            # Still not matching.
            # Let me just try sorting by value for negative numbers and see if that matches.
            # Actually, looking at the expected output [-6, -5, -4, -3, -2], this is just sorted ascending.
            # Maybe the problem expects that for negative numbers, we just sort by value?
            # Or maybe I'm overthinking this. Let me just use bin(n) and count the '1's in the string.
            s = bin(n)
            return s.count('1')
        else:
            return bin(n).count('1')
    
    return sorted(arr, key=lambda x: (count_ones(x), x))

def check(candidate):

    # Check some simple cases
    assert True, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate([1,5,2,3,4]) == [1, 2, 4, 3, 5]
    assert candidate([-2,-3,-4,-5,-6]) == [-4, -2, -6, -5, -3]
    assert candidate([1,0,2,3,4]) == [0, 1, 2, 4, 3]
    assert candidate([]) == []
    assert candidate([2,5,77,4,5,3,5,7,2,3,4]) == [2, 2, 4, 4, 3, 3, 5, 5, 5, 7, 77]
    assert candidate([3,6,44,12,32,5]) == [32, 3, 5, 6, 12, 44]
    assert candidate([2,4,8,16,32]) == [2, 4, 8, 16, 32]
    assert candidate([2,4,8,16,32]) == [2, 4, 8, 16, 32]

    # Check some edge cases that are easy to work out by hand.
    assert True, "This prints if this assert fails 2 (also good for debugging!)"


check(sort_array)
print('PASS_ba751d983a504873b5920bbb29e31f0a')
