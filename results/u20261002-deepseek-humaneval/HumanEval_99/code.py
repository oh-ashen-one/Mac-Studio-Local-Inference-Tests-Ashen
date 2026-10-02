def closest_integer(value):
    from decimal import Decimal, ROUND_HALF_UP
    return int(Decimal(value).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
