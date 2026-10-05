def car_race_collision(n: int):
    """
    Imagine a road that's a perfectly straight infinitely long line.
    n cars are driving left to right;  simultaneously, a different set of n cars
    are driving right to left.   The two sets of cars start out being very far from
    each other.  All cars move in the same speed.  Two cars are said to collide
    when a car that's moving left to right hits a car that's moving right to left.
    However, the cars are infinitely sturdy and strong; as a result, they continue moving
    in their trajectory as if they did not collide.

    This function outputs the number of such collisions.
    """
    # Every car moving left-to-right will eventually cross paths with 
    # every car moving right-to-left because they start far apart 
    # and move towards each other on a 1D line.
    # There are n cars moving L->R and n cars moving R->L.
    # Total collisions = n * n
    return n * n
