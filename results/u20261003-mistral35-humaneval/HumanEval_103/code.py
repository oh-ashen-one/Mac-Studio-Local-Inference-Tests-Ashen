def rounded_avg(n, m):
    if n > m:
        return -1
    total = (m - n + 1) * (n + m) // 2
    average = total / (m - n + 1)
    rounded = round(average)
    return bin(rounded)
