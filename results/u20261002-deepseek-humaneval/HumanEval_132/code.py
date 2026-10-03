def is_nested(string):
    open_count = 0
    max_open = 0
    for ch in string:
        if ch == '[':
            open_count += 1
            max_open = max(max_open, open_count)
        else:
            if open_count > 0:
                open_count -= 1
    return max_open >= 2
