import math

def max_fill(grid, capacity):
    """
    Calculates the total number of bucket lowers needed to empty all wells.
    Each row in the grid is a well. The number of 1s in a row is the amount of water.
    The number of lowers for a single well is ceil(water_in_well / capacity).
    """
    total_lowers = 0
    for row in grid:
        water_amount = sum(row)
        if water_amount > 0:
            total_lowers += math.ceil(water_amount / capacity)
    return total_lowers
