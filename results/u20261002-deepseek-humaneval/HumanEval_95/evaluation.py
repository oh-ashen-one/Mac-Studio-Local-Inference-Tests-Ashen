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


def check_dict_case(dict):
    """
    Given a dictionary, return True if all keys are strings in lower 
    case or all keys are strings in upper case, else return False.
    The function should return False is the given dictionary is empty.
    Examples:
    check_dict_case({"a":"apple", "b":"banana"}) should return True.
    check_dict_case({"a":"apple", "A":"banana", "B":"banana"}) should return False.
    check_dict_case({"a":"apple", 8:"banana", "a":"apple"}) should return False.
    check_dict_case({"Name":"John", "Age":"36", "City":"Houston"}) should return False.
    check_dict_case({"STATE":"NC", "ZIP":"12345" }) should return True.
    """

def check_dict_case(dict):
    if not dict:
        return False
    keys = list(dict.keys())
    if all(isinstance(k, str) and k.islower() for k in keys):
        return True
    if all(isinstance(k, str) and k.isupper() for k in keys):
        return True
    return False

def check(candidate):

    # Check some simple cases
    assert candidate({"p":"pineapple", "b":"banana"}) == True, "First test error: " + str(candidate({"p":"pineapple", "b":"banana"}))
    assert candidate({"p":"pineapple", "A":"banana", "B":"banana"}) == False, "Second test error: " + str(candidate({"p":"pineapple", "A":"banana", "B":"banana"}))
    assert candidate({"p":"pineapple", 5:"banana", "a":"apple"}) == False, "Third test error: " + str(candidate({"p":"pineapple", 5:"banana", "a":"apple"}))
    assert candidate({"Name":"John", "Age":"36", "City":"Houston"}) == False, "Fourth test error: " + str(candidate({"Name":"John", "Age":"36", "City":"Houston"}))
    assert candidate({"STATE":"NC", "ZIP":"12345" }) == True, "Fifth test error: " + str(candidate({"STATE":"NC", "ZIP":"12345" }))      
    assert candidate({"fruit":"Orange", "taste":"Sweet" }) == True, "Fourth test error: " + str(candidate({"fruit":"Orange", "taste":"Sweet" }))      


    # Check some edge cases that are easy to work out by hand.
    assert candidate({}) == False, "1st edge test error: " + str(candidate({}))


check(check_dict_case)
print('PASS_27c6ce2cbe9e48909427257659f724ac')
