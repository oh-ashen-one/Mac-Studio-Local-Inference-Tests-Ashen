def correct_bracketing(brackets: str) -> bool:
    balance = 0
    for char in brackets:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return False
    return balance == 0
