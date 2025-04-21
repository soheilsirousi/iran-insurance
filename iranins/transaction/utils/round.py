
def round_to_nearest(amount):
    remainder = amount % 50000
    return amount - remainder, remainder
