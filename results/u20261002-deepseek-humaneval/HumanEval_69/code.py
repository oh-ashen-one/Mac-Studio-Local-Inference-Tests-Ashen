from collections import Counter

def search(lst):
    freq = Counter(lst)
    result = -1
    for num, count in freq.items():
        if count >= num and num > result:
            result = num
    return result
