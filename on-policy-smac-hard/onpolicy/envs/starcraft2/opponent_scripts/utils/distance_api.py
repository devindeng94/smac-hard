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

def toward(us, ut, d):
    if isinstance(us, tuple):
        xs, ys = us
    else:
        xs, ys = us.pos.x, us.pos.y
    if isinstance(ut, tuple):
        xt, yt = ut
    else:
        xt, yt = ut.pos.x, ut.pos.y
    dis = distance_to((xs, ys), (xt, yt))
    return (xs + (xt - xs)/dis*d, ys + (yt - ys)/dis*d)

def in_map_bounds(pos, map_state):
    return pos[0] < map_state.x and pos[1] < map_state.y

def get_direction(p1, p2):
    diff = [p2[0]-p1[0], p2[1]-p1[1]]
    length = math.hypot(diff[0], diff[1])
    return [diff[0]/length, diff[1]/length]


def closer_than(target, candidate, dist):

    closer = []
    for c in candidate:
        if distance_to(c, target) <= dist:
            closer.append(c)
    return closer