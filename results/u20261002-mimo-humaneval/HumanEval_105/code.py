def by_length(arr):
    names = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    filtered = sorted(x for x in arr if 1 <= x <= 9)
    filtered.reverse()
    return [names[x - 1] for x in filtered]
