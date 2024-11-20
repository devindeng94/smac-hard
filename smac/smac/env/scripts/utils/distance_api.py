import math

def distance_to(unit_from, unit_to):

    if type(unit_from) == tuple:
        x1 = unit_from[0]
        y1 = unit_from[1]
    else:
        x1 = unit_from.pos.x
        y1 = unit_from.pos.y

    if type(unit_to) == tuple:
        x2 = unit_to[0]
        y2 = unit_to[1]
    else:
        x2 = unit_to.pos.x
        y2 = unit_to.pos.y

    delta_x = x1 - x2
    delta_y = y1 - y2

    return math.sqrt(delta_x ** 2 + delta_y ** 2)


def nearest_n_units(target, candidates, num):

    if len(candidates) <= num:
        return candidates

    return sorted(candidates, key=lambda e: distance_to(e, target))[:num]

def toward(us, ut, dis):
    xs, ys = us.pos.x, us.pos.y
    xt, yt = ut.pos.x, ut.pos.y
    dis = min(dis, distance_to((xs, ys), (xt, yt)))
    return (xs + (xt - xs)/dis, ys + (yt - ys)/dis)