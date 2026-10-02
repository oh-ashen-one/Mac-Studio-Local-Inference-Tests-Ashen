def match_parens(lst):
    def is_good(s):
        balance = 0
        for c in s:
            if c == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                return False
        return balance == 0
    
    def can_concatenate(a, b):
        # Try a + b
        balance = 0
        valid = True
        for c in a:
            if c == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                valid = False
                break
        if valid:
            for c in b:
                if c == '(':
                    balance += 1
                else:
                    balance -= 1
                if balance < 0:
                    valid = False
                    break
            if valid and balance == 0:
                return True
        
        # Try b + a
        balance = 0
        valid = True
        for c in b:
            if c == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                valid = False
                break
        if valid:
            for c in a:
                if c == '(':
                    balance += 1
                else:
                    balance -= 1
                if balance < 0:
                    valid = False
                    break
            if valid and balance == 0:
                return True
        
        return False
    
    return 'Yes' if can_concatenate(lst[0], lst[1]) else 'No'
