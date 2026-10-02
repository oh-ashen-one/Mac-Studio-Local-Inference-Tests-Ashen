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


def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """

def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    if n == 1:
        # 1-digit numbers: 1 through 9. Those that start or end with 1: just 1.
        return 1
    
    # n-digit numbers range from 10^(n-1) to 10^n - 1
    # Count numbers that start with 1:
    #   First digit is 1, remaining n-1 digits can be anything (0-9)
    #   So 1 * 10^(n-1) numbers
    # Count numbers that end with 1:
    #   Last digit is 1, first digit can be 1-9 (9 choices), middle n-2 digits can be 0-9
    #   So 9 * 10^(n-2) numbers
    # But we double-counted numbers that both start AND end with 1:
    #   First digit is 1, last digit is 1, middle n-2 digits can be anything
    #   So 1 * 10^(n-2) numbers
    # By inclusion-exclusion: start_with_1 + end_with_1 - both
    # = 10^(n-1) + 9 * 10^(n-2) - 10^(n-2)
    # = 10^(n-1) + 8 * 10^(n-2)
    
    if n == 1:
        return 1
    
    start_with_1 = 10 ** (n - 1)
    end_with_1 = 9 * (10 ** (n - 2))
    both = 10 ** (n - 2)
    
    return start_with_1 + end_with_1 - both

def check(candidate):

    # Check some simple cases
    assert True, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate(1) == 1
    assert candidate(2) == 18
    assert candidate(3) == 180
    assert candidate(4) == 1800
    assert candidate(5) == 18000

    # Check some edge cases that are easy to work out by hand.
    assert True, "This prints if this assert fails 2 (also good for debugging!)"


check(starts_one_ends)
print('PASS_b18c8356be12402ba3f3147ad376ca14')
