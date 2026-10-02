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
print('PASS_c2a69f31b6254312800210486eee8ede')
