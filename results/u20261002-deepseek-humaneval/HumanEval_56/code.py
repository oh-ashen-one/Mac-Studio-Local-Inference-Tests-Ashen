def correct_bracketing(brackets: str):
    balance = 0
    for b in brackets:
        if b == "<":
            balance += 1
        elif b == ">":
            balance -= 1
            if balance < 0:
                return False
    return balance == 0
