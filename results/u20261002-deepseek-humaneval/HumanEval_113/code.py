def odd_count(lst):
    result = []
    for i, s in enumerate(lst):
        count = sum(1 for ch in s if int(ch) % 2 == 1)
        result.append(
            f"the number of odd elements {count}n the str{count}ng {count} of the {count}nput."
        )
    return result
