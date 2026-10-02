def rounded_avg(n, m):
    if n > m:
        return -1
    total = (n + m) * (m - n + 1) // 2
    count = m - n + 1
    avg = total / count
    rounded = round(avg)
    return bin(rounded)
