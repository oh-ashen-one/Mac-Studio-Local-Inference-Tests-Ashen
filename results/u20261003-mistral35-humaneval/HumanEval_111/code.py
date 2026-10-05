from collections import Counter

def histogram(test):
    if not test:
        return {}
    counts = Counter(test.split())
    max_count = max(counts.values())
    return {k: v for k, v in counts.items() if v == max_count}
