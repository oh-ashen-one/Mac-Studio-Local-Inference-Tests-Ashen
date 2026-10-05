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


def any_int(x, y, z):
    '''
    Create a function that takes 3 numbers.
    Returns true if one of the numbers is equal to the sum of the other two, and all numbers are integers.
    Returns false in any other cases.
    
    Examples
    any_int(5, 2, 7) ➞ True
    
    any_int(3, 2, 2) ➞ False

    any_int(3, -2, 1) ➞ True
    
    any_int(3.6, -2.2, 2) ➞ False
  

    
    '''

def any_int(x, y, z):
    '''
    Create a function that takes 3 numbers.
    Returns true if one of the numbers is equal to the sum of the other two, and all numbers are integers.
    Returns false in any other cases.
    '''
    if not all(isinstance(num, int) for num in (x, y, z)):
        return False
    return x == y + z or y == x + z or z == x + y

def check(candidate):

    # Check some simple cases
    assert candidate(2, 3, 1)==True, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate(2.5, 2, 3)==False, "This prints if this assert fails 2 (good for debugging!)"
    assert candidate(1.5, 5, 3.5)==False, "This prints if this assert fails 3 (good for debugging!)"
    assert candidate(2, 6, 2)==False, "This prints if this assert fails 4 (good for debugging!)"
    assert candidate(4, 2, 2)==True, "This prints if this assert fails 5 (good for debugging!)"
    assert candidate(2.2, 2.2, 2.2)==False, "This prints if this assert fails 6 (good for debugging!)"
    assert candidate(-4, 6, 2)==True, "This prints if this assert fails 7 (good for debugging!)"

    # Check some edge cases that are easy to work out by hand.
    assert candidate(2,1,1)==True, "This prints if this assert fails 8 (also good for debugging!)"
    assert candidate(3,4,7)==True, "This prints if this assert fails 9 (also good for debugging!)"
    assert candidate(3.0,4,7)==False, "This prints if this assert fails 10 (also good for debugging!)"


check(any_int)
print('PASS_45ebb73c5eab4088931f206fed6646bd')
