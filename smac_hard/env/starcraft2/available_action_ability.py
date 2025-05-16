import numpy as np
import math
import pdb

ability_dict ={
    380:    ('self', 3675, 0),  # Effect_Stim_quick
    1664:   ('ally', 1664, 7),  # Effect_Transfusion_screen
    2393:   ('self', 2393, 0),  # Effect_VoidRayPrismaticAlignment_quick
    1998:   ('self', 1998, 0),  # Morph_Hellbat_quick
    1978:   ('self', 1978, 0),  # Morph_Hellbat_quick
    2588:   ('point', 2588, 5), # Effect_KD8Charge_screen
    1442:   ('point', 3687, 8), # Effect_Blink_Stalker_screen
    388:    ('self', 388, 0),   # Morph_SiegeMode_quick
    253:    ('self', 3675, 0),  # Effect_Stim_Marauder_quick
    2116:   ('self', 2116, 0),  # Effect_MedivacIgniteAfterburners_quick
    390:    ('self', 390, 0),   # Morph_Unsiege_quick
    }


def distance(x1, y1, x2, y2):
    """Distance between two points."""
    return math.hypot(x2 - x1, y2 - y1)

def check_bounds(x, y, map_x, map_y):
    """Whether a point is within the map bounds."""
    if 0 <= x < map_x and 0 <= y < map_y:
        return 1
    else:
        return 0

# Self unit, 
def avail_ability(self, units, targets, ability_id, map_x, map_y):
    n_actions = max(len(units), len(targets), 9)
    avail_actions = [0] * n_actions

    if ability_id in [380, 2393, 1998, 1978, 388, 253, 2116, 390]:
        avail_actions[0] = 1
    elif ability_id == 1664:  
        # Transfusion, attack ALLY units except SELF, DAMAGED, within range 7
        for u_idx, unit in units.items():
            if self.tag == unit.tag:
                continue
            if unit.health != unit.health_max and distance(self.pos.x, self.pos.y, unit.pos.x, unit.pos.y) < 7:
                avail_actions[u_idx] = 1

    elif ability_id in [2588, 1442]:
        ability_range = math.ceil(ability_dict[ability_id][2] / 2)
        x, y = self.pos.x, self.pos.y

        surroundings = []
        surroundings.append((x, y))
        surroundings.append((x, y + ability_range))
        surroundings.append((x + ability_range/2, y + ability_range/2))
        surroundings.append((x + ability_range, y))
        surroundings.append((x + ability_range/2, y - ability_range/2))
        surroundings.append((x, y - ability_range/2))
        surroundings.append((x - ability_range/2, y - ability_range/2))
        surroundings.append((x - ability_range, y))
        surroundings.append((x - ability_range/2, y + ability_range/2))
        for i in range(9):
            avail_actions[i] = check_bounds(*surroundings[i], map_x, map_y)

    
    return avail_actions