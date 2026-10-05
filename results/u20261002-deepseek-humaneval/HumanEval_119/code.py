def match_parens(lst):
    def is_good(s):
        bal = 0
        for ch in s:
            if ch == '(':
                bal += 1
            else:
                bal -= 1
            if bal < 0:
                return False
        return bal == 0

    return 'Yes' if is_good(lst[0] + lst[1]) or is_good(lst[1] + lst[0]) else 'No'
