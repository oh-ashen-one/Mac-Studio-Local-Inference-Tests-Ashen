def fizz_buzz(n: int) -> int:
    """Return the number of times the digit 7 appears in integers less than n which are divisible by 11 or 13."""
    count = 0
    for num in range(n):
        if num % 11 == 0 or num % 13 == 0:
            count += str(num).count('7')
    return count
