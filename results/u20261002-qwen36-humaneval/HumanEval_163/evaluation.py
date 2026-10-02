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


def generate_integers(a, b):
    """
    Given two positive integers a and b, return the even digits between a
    and b, in ascending order.

    For example:
    generate_integers(2, 8) => [2, 4, 6, 8]
    generate_integers(8, 2) => [2, 4, 6, 8]
    generate_integers(10, 14) => []
    """

def generate_integers(a, b):
    """
    Given two positive integers a and b, return the even digits between a
    and b, in ascending order.

    For example:
    generate_integers(2, 8) => [2, 4, 6, 8]
    generate_integers(8, 2) => [2, 4, 6, 8]
    generate_integers(10, 14) => []
    """
    # Determine the range
    start = min(a, b)
    end = max(a, b)
    
    # Collect even digits from 0-9 that appear in numbers within the range
    # But wait, re-reading the spec: "return the even digits between a and b"
    # Looking at examples:
    # generate_integers(2, 8) => [2, 4, 6, 8] - these are even numbers between 2 and 8
    # generate_integers(8, 2) => [2, 4, 6, 8] - same, sorted ascending
    # generate_integers(10, 14) => [] - even numbers between 10 and 14 are 10, 12, 14, but result is []
    
    # Hmm, 10, 12, 14 are even numbers between 10 and 14. But the result is [].
    # So it's not about even numbers. It's about even DIGITS.
    
    # Let me re-read: "return the even digits between a and b"
    # For 2 to 8: the even digits that appear in any number from 2 to 8?
    # Numbers 2,3,4,5,6,7,8 contain digits: 2,3,4,5,6,7,8. Even digits: 2,4,6,8.
    # For 10 to 14: numbers 10,11,12,13,14. Digits: 1,0,1,1,1,2,1,3,1,4. Even digits: 0,2,4.
    # But result is [].
    
    # Wait, maybe "even digits" means single-digit even numbers? 0,2,4,6,8?
    # For 10-14, the digits include 0,2,4. But result is [].
    
    # Let me think differently. Maybe it's about which even digits (0,2,4,6,8) are "between" a and b?
    # For 2-8: even digits 2,4,6,8 are all between 2 and 8. Result: [2,4,6,8].
    # For 10-14: even digits 0,2,4,6,8. Which are between 10 and 14? None of 0,2,4,6,8 are between 10 and 14. Result: [].
    
    # That makes sense! The even digits are 0, 2, 4, 6, 8. We return those that fall within [start, end].
    
    even_digits = [0, 2, 4, 6, 8]
    result = [d for d in even_digits if start <= d <= end]
    return result

def check(candidate):

    # Check some simple cases
    assert candidate(2, 10) == [2, 4, 6, 8], "Test 1"
    assert candidate(10, 2) == [2, 4, 6, 8], "Test 2"
    assert candidate(132, 2) == [2, 4, 6, 8], "Test 3"
    assert candidate(17,89) == [], "Test 4"

    # Check some edge cases that are easy to work out by hand.
    assert True, "This prints if this assert fails 2 (also good for debugging!)"


check(generate_integers)
print('PASS_5a740ac10cb547bd9eda21934e6dd671')
