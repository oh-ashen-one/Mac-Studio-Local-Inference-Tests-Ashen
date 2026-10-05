from collections import Counter

def search(lst):
    freq = Counter(lst)
    result = -1
    for num, count in freq.items():
        if num > 0 and count >= num:
            if num > result:
                result = num
    return result
