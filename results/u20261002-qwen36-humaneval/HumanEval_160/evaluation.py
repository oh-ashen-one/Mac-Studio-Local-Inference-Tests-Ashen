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


def do_algebra(operator, operand):
    """
    Given two lists operator, and operand. The first list has basic algebra operations, and 
    the second list is a list of integers. Use the two given lists to build the algebric 
    expression and return the evaluation of this expression.

    The basic algebra operations:
    Addition ( + ) 
    Subtraction ( - ) 
    Multiplication ( * ) 
    Floor division ( // ) 
    Exponentiation ( ** ) 

    Example:
    operator['+', '*', '-']
    array = [2, 3, 4, 5]
    result = 2 + 3 * 4 - 5
    => result = 9

    Note:
        The length of operator list is equal to the length of operand list minus one.
        Operand is a list of of non-negative integers.
        Operator list has at least one operator, and operand list has at least two operands.

    """

import operator as op_module
from functools import reduce

def do_algebra(operator, operand):
    """
    Given two lists operator, and operand. The first list has basic algebra operations, and 
    the second list is a list of integers. Use the two given lists to build the algebric 
    expression and return the evaluation of this expression.

    The basic algebra operations:
    Addition ( + ) 
    Subtraction ( - ) 
    Multiplication ( * ) 
    Floor division ( // ) 
    Exponentiation ( ** ) 

    Example:
    operator['+', '*', '-']
    array = [2, 3, 4, 5]
    result = 2 + 3 * 4 - 5
    => result = 9

    Note:
        The length of operator list is equal to the length of operand list minus one.
        Operand is a list of of non-negative integers.
        Operator list has at least one operator, and operand list has at least two operands.

    """
    # Map operator strings to actual functions
    op_map = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '//': lambda a, b: a // b,
        '**': lambda a, b: a ** b,
    }
    
    # Build the expression by applying operators sequentially
    # Since we need to respect operator precedence, we can't just reduce left-to-right
    # We need to parse the expression properly.
    
    # Let's build a list of (operand, operator) pairs and then evaluate with proper precedence.
    # The expression is: operand[0] op[0] operand[1] op[1] operand[2] ... op[n-1] operand[n]
    
    # To handle operator precedence correctly:
    # ** has highest precedence, then *, //, then +, -
    # We can use a stack-based approach (Shunting Yard or similar)
    
    # Let's create tokens: operands and operators
    tokens = []
    for i in range(len(operand)):
        tokens.append(('num', operand[i]))
        if i < len(operator):
            tokens.append(('op', operator[i]))
    
    # Remove the last operator if it exists (there should be n-1 operators for n operands)
    # Actually, tokens will be: num, op, num, op, ..., num
    # So we have 2*n - 1 tokens
    
    # Now evaluate with proper precedence
    # Use two stacks: values and ops
    values = []
    ops = []
    
    def apply_op():
        if not ops:
            return
        op = ops.pop()
        b = values.pop()
        a = values.pop()
        func = op_map[op]
        values.append(func(a, b))
    
    i = 0
    while i < len(tokens):
        token_type, token_val = tokens[i]
        if token_type == 'num':
            values.append(token_val)
        else:
            # It's an operator
            current_op = token_val
            # While there's an operator on top of ops stack with greater or equal precedence
            # (except for ** which is right-associative)
            while ops:
                top_op = ops[-1]
                # Check precedence
                prec = {'**': 4, '*': 3, '//': 3, '+': 2, '-': 2}
                top_prec = prec.get(top_op, 0)
                curr_prec = prec.get(current_op, 0)
                
                if top_prec >= curr_prec:
                    # For ** which is right-associative, we don't apply if equal
                    if current_op == '**' and top_op == '**':
                        break
                    apply_op()
                else:
                    break
            ops.append(current_op)
        i += 1
    
    # Apply remaining operators
    while ops:
        apply_op()
    
    return values[0]

def check(candidate):

    # Check some simple cases
    assert candidate(['**', '*', '+'], [2, 3, 4, 5]) == 37
    assert candidate(['+', '*', '-'], [2, 3, 4, 5]) == 9
    assert candidate(['//', '*'], [7, 3, 4]) == 8, "This prints if this assert fails 1 (good for debugging!)"

    # Check some edge cases that are easy to work out by hand.
    assert True, "This prints if this assert fails 2 (also good for debugging!)"


check(do_algebra)
print('PASS_98be5550266f43f7bc2885e678fb8f0c')
