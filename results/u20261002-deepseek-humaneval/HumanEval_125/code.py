def split_words(txt):
    if ' ' in txt:
        return txt.split()
    if ',' in txt:
        return txt.split(',')
    return sum(1 for ch in txt if ch.islower() and (ord(ch) - ord('a')) % 2 == 1)
