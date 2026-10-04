def intersection(interval1, interval2):
    start1, end1 = interval1
    start2, end2 = interval2
    start = max(start1, start2)
    end = min(end1, end2)
    if start > end:
        return "NO"
    length = end - start + 1
    if length < 2:
        return "NO"
    for i in range(2, int(length ** 0.5) + 1):
        if length % i == 0:
            return "NO"
    return "YES"
