from itertools import combinations

def triples_sum_to_zero(l: list):
    for combo in combinations(l, 3):
        if sum(combo) == 0:
            return True
    return False
