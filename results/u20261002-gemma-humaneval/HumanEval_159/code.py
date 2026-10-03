def eat(number, need, remaining):
    """
    You're a hungry rabbit, and you already have eaten a certain number of carrots,
    but now you need to eat more carrots to complete the day's meals.
    you should return an array of [ total number of eaten carrots after your meals,
                                    the number of carrots left after your meals ]
    if there are not enough remaining carrots, you will eat all remaining carrots, but will still be hungry.
    """
    amount_to_eat = min(need, remaining)
    total_eaten = number + amount_to_eat
    left_over = remaining - amount_to_eat
    return [total_eaten, left_over]
