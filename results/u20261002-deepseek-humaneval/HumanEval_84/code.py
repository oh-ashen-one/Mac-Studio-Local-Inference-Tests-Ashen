def solve(N):
    digit_sum = sum(int(d) for d in str(N))
    return bin(digit_sum)[2:]
