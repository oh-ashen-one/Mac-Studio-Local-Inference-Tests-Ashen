def match_parens(lst):
    s1, s2 = lst

    def is_balanced(s):
        balance = 0
        for char in s:
            if char == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                return False
        return balance == 0

    def can_form_balanced(a, b):
        total_balance = 0
        min_balance = 0
        for char in a + b:
            if char == '(':
                total_balance += 1
            else:
                total_balance -= 1
            if total_balance < min_balance:
                min_balance = total_balance
        return total_balance == 0 and min_balance >= 0

    if can_form_balanced(s1, s2) or can_form_balanced(s2, s1):
        return 'Yes'
    return 'No'
