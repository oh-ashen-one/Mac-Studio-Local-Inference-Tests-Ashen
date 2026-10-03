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


def simplify(x, n):
    """Your task is to implement a function that will simplify the expression
    x * n. The function returns True if x * n evaluates to a whole number and False
    otherwise. Both x and n, are string representation of a fraction, and have the following format,
    <numerator>/<denominator> where both numerator and denominator are positive whole numbers.

    You can assume that x, and n are valid fractions, and do not have zero as denominator.

    simplify("1/5", "5/1") = True
    simplify("1/6", "2/1") = False
    simplify("7/10", "10/2") = False
    """

def simplify(x, n):
    """
    Simplify the expression x * n.
    Returns True if x * n evaluates to a whole number, False otherwise.
    
    Both x and n are string representations of fractions in the format <numerator>/<denominator>.
    """
    # Parse x
    x_num, x_den = map(int, x.split('/'))
    # Parse n
    n_num, n_den = map(int, n.split('/'))
    
    # Compute x * n = (x_num * n_num) / (x_den * n_den)
    numerator = x_num * n_num
    denominator = x_den * n_den
    
    # Check if the result is a whole number
    # i.e., numerator % denominator == 0
    return numerator % denominator == 0

def check(candidate):

    # Check some simple cases
    assert candidate("1/5", "5/1") == True, 'test1'
    assert candidate("1/6", "2/1") == False, 'test2'
    assert candidate("5/1", "3/1") == True, 'test3'
    assert candidate("7/10", "10/2") == False, 'test4'
    assert candidate("2/10", "50/10") == True, 'test5'
    assert candidate("7/2", "4/2") == True, 'test6'
    assert candidate("11/6", "6/1") == True, 'test7'
    assert candidate("2/3", "5/2") == False, 'test8'
    assert candidate("5/2", "3/5") == False, 'test9'
    assert candidate("2/4", "8/4") == True, 'test10'


    # Check some edge cases that are easy to work out by hand.
    assert candidate("2/4", "4/2") == True, 'test11'
    assert candidate("1/5", "5/1") == True, 'test12'
    assert candidate("1/5", "1/5") == False, 'test13'


check(simplify)
print('PASS_de4df795edb04b1b99cd7851b39fb601')
