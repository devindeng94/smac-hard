import math

def distance_to(unit_from, unit_to):
    if type(unit_from) == tuple and type(unit_to) == tuple:
        delta_x = unit_from[0] - unit_to[0]
        delta_y = unit_from[1] - unit_to[1]
    else:
        delta_x = unit_from.pos.x - unit_to.pos.x
        delta_y = unit_from.pos.y - unit_to.pos.y

    return math.sqrt(delta_x ** 2 + delta_y ** 2)


def nearest_n_units(target, candidates, num):

    if len(candidates) <= num:
        return candidates

    return sorted(candidates, key=lambda e: distance_to(e, target))[:num]