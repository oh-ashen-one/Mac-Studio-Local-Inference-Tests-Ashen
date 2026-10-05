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


def can_arrange(arr):
    """Create a function which returns the largest index of an element which
    is not greater than or equal to the element immediately preceding it. If
    no such element exists then return -1. The given array will not contain
    duplicate values.

    Examples:
    can_arrange([1,2,4,3,5]) = 3
    can_arrange([1,2,3]) = -1
    """

def can_arrange(arr):
    for i in range(len(arr) - 1, 0, -1):
        if arr[i] < arr[i - 1]:
            return i
    return -1

def check(candidate):

    # Check some simple cases
    assert candidate([1,2,4,3,5])==3
    assert candidate([1,2,4,5])==-1
    assert candidate([1,4,2,5,6,7,8,9,10])==2
    assert candidate([4,8,5,7,3])==4

    # Check some edge cases that are easy to work out by hand.
    assert candidate([])==-1


check(can_arrange)
print('PASS_380d156db8ea45f3b6a89327e4adce0c')
