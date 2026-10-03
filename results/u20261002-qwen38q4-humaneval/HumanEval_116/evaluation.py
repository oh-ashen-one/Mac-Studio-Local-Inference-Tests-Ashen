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
print('PASS_6ff607a50855486fa8d17f3d085dc1dc')
