def get_odd_collatz(n):
    """
    Given a positive integer n, return a sorted list that has the odd numbers in collatz sequence.
    """
    odd_numbers = set()
    current = n
    while current != 1:
        if current % 2 != 0:
            odd_numbers.add(current)
        if current % 2 == 0:
            current = current // 2
        else:
            current = 3 * current + 1
    odd_numbers.add(1)  # 1 is always part of the sequence and is odd
    return sorted(odd_numbers)
