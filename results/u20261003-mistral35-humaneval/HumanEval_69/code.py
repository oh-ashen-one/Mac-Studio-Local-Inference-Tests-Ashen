from collections import Counter

def search(lst):
    counts = Counter(lst)
    candidates = [num for num in counts if counts[num] >= num and num > 0]
    return max(candidates) if candidates else -1
