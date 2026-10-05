def split_words(txt):
    if ' ' in txt:
        return txt.split()
    elif ',' in txt:
        return txt.split(',')
    else:
        count = 0
        for ch in txt:
            if ch.islower():
                idx = ord(ch) - ord('a')
                if idx % 2 == 1:
                    count += 1
        return count
