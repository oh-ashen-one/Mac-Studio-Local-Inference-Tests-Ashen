def do_algebra(operator, operand):
    """
    Given two lists operator, and operand. The first list has basic algebra operations, and 
    the second list is a list of integers. Use the two given lists to build the algebric 
    expression and return the evaluation of this expression.
    """
    # Build the expression string by interleaving operands and operators
    expression = str(operand[0])
    for i in range(len(operator)):
        expression += f" {operator[i]} {operand[i+1]}"
    
    # eval() handles the standard Python operator precedence (PEMDAS)
    # which matches the requirements for basic algebra operations.
    return eval(expression)
