def vowels_count(s):
    vowels = set('aeiouAEIOU')
    count = 0
    for i, ch in enumerate(s):
        if ch in vowels:
            count += 1
        elif ch.lower() == 'y' and i == len(s) - 1:
            count += 1
    return count
