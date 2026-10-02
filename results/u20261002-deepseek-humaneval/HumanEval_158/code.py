def find_max(words):
    return max(words, key=lambda w: (len(set(w)), [-ord(c) for c in w]))
