import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name

    def script(self, obs, iteration):
        
        self.actions_list = []
        units = [unit for unit in obs.observation.raw_data.units if unit.owner==2]
        enemy_units = [unit for unit in obs.observation.raw_data.units if unit.owner==1]

        marines = sorted([unit for unit in units if unit.unit_type==UnitTypeId.MARINE.value], key=lambda u: u.tag)
        enemy_marines = [unit for unit in enemy_units if unit.unit_type==MAP_UNITS_TYPES[self.map_name]['enemy'][0]]
        
        if not marines or not enemy_marines:
            return []
        
        if iteration < 5:
            self.update_formation(marines)
            return self.actions_list
        
        # Move left
        if min([distance_to(center(marines), em) for em in enemy_marines]) > 9:
            for marine in marines:
                self.actions_list.append(move_point(marine, marine.pos.x-2, marine.pos.y))
        else:
            for marine in marines:
                target = nearest_n_units(marine, enemy_marines, 5)
                weakest_target = min(target, key=lambda e: e.health)

                self.actions_list.append(attack(marine, (weakest_target.pos.x, weakest_target.pos.y)))

        return self.actions_list

    def update_formation(self, marines):

        marines_sorted = sorted(marines, key=lambda m: m.pos.y)

        for i, marine in enumerate(marines_sorted):
            position = (25, 16 + (i - len(marines) / 2) * 0.65)
            self.actions_list.append(move_point(marine, position[0], position[1]))
        self.formation = marines_sorted
    
        