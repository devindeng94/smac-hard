import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

MOVE_AMOUNT = 2
SHOOT_RANGE = 6

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name

    def script(self, obs, iteration):
        self.actions_list = []

        units = [unit for unit in obs.observation.raw_data.units if unit.owner==2]
        enemy_units = [unit for unit in obs.observation.raw_data.units if unit.owner==1]

        stalkers = [unit for unit in units if unit.unit_type==UnitTypeId.STALKER.value]
        zealots = [unit for unit in units if unit.unit_type==UnitTypeId.ZEALOT.value]

        enemy_zealots = sorted([unit for unit in enemy_units if unit.unit_type==MAP_UNITS_TYPES[self.map_name]['enemy'][1]], key=lambda u:u.tag)
        enemy_stalkers = sorted([unit for unit in enemy_units if unit.unit_type==MAP_UNITS_TYPES[self.map_name]['enemy'][0]], key=lambda u:u.tag)
        
        if not enemy_zealots and not enemy_stalkers:
            return []

        if not units:
            return []

        # Stalker attack zealot first
        if enemy_zealots:
            target = nearest_n_units(center(units), enemy_zealots, 1)[0]
        elif enemy_stalkers:
            target = nearest_n_units(center(units), enemy_stalkers, 1)[0]
        else:
            target = center(enemy_units)

        for stalker in stalkers:
            if stalker.health/stalker.health_max < 0.5:
                # Retreat to starting point
                self.actions_list.append(move(stalker, (23, 16)))
            else:
                self.actions_list.append(attack(stalker, target))

        target = nearest_n_units(center(units), enemy_units, 1)[0]
        for zealot in zealots:
            if zealot.health/zealot.health_max < 0.5:
                self.actions_list.append(move(zealot, (23, 16)))
            else:
                self.actions_list.append(attack(zealot, target))
            
        return self.actions_list

