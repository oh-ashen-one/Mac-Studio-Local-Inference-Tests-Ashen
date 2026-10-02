def do_algebra(operator, operand):
    result = operand[0]
    for op, num in zip(operator, operand[1:]):
        if op == '+':
            result += num
        elif op == '-':
            result -= num
        elif op == '*':
            result *= num
        elif op == '//':
            result //= num
        elif op == '**':
            result **= num
    return result
