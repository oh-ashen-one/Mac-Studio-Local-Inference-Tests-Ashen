def solve(N):
    """Given a positive integer N, return the total sum of its digits in binary."""
    digit_sum = sum(int(d) for d in str(N))
    return bin(digit_sum)[2:]
