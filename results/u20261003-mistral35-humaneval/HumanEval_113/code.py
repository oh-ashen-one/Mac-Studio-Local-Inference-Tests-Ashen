def odd_count(lst):
    result = []
    for s in lst:
        count = sum(1 for c in s if int(c) % 2 != 0)
        template = f"the number of odd elements {count}n the str{count}ng {count} of the {count}nput."
        result.append(template)
    return result
