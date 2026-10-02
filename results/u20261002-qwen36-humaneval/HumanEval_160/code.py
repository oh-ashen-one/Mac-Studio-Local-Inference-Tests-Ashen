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
