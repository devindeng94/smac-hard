import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        self.map_name = map_name
        
        
    def script(self, obs, iteration):

        actions_list = []
        
        marines = [unit for unit in obs.observation.raw_data.units if unit.owner==1]
        enemy_zealot = [unit for unit in obs.observation.raw_data.units if unit.owner==2][0]
        
        # Iterate over the marines
        for marine in marines:
            # Kite the zealot by the distance
            if distance_to(marine, enemy_zealot) < 3 and enemy_zealot.health > 30:
                # Calculate the retreate position
                retreat_position = toward(marine, enemy_zealot, -5)
                map_state = obs.observation.raw_data.map_state.visibility.size
                # Determine if the retreat position is within the map
                if not in_map_bounds(retreat_position, map_state):
                    # Change a direction to retreate
                    direction = get_direction(enemy_zealot.pos, marine.pos)
                    angle = math.pi / 4
                    rotated_direction = (direction[0] * math.cos(angle) - direction[1] * math.sin(angle),
                                            direction[0] * math.sin(angle) + direction[1] * math.cos(angle))
                    retreat_position = [enemy_zealot.pos.x + rotated_direction[0] * 5, enemy_zealot.pos.y + rotated_direction[1] * 5]
                actions_list.append(move(marine, retreat_position))
            # Fire focus on the target enemy
            else:
                actions_list.append(attack(marine, enemy_zealot))

        return actions_list
