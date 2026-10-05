def get_odd_collatz(n):
    """
    Given a positive integer n, return a sorted list that has the odd numbers in collatz sequence.
    """
    odds = []
    current = n
    while True:
        if current % 2 != 0:
            odds.append(current)
        if current == 1:
            break
        if current % 2 == 0:
            current //= 2
        else:
            current = 3 * current + 1
    
    return sorted(odds)
