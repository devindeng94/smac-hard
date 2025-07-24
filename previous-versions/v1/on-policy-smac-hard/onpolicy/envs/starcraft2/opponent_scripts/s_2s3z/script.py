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
        actions_list = []

        stalkers = [unit for unit in units if unit.unit_type==UnitTypeId.STALKER.value]
        zealots = [unit for unit in units if unit.unit_type==UnitTypeId.ZEALOT.value]


        for stalker in stalkers:
            closest_enemy = nearest_n_units(stalker, enemy_units, 1)[0]

            if distance_to(stalker, closest_enemy) > SHOOT_RANGE:
                self.actions_list.append(attack(stalker, closest_enemy))
            elif stalker.health/stalker.health_max < 0.5:
                self.actions_list.append(move(stalker, (23, 16)))
            else:
                self.actions_list.append(attack(stalker, closest_enemy))

        for zealot in zealots:
            closest_enemy = nearest_n_units(zealot, enemy_units, 1)[0]

            if distance_to(zealot, closest_enemy) > 0.1:
                self.actions_list.append(attack(zealot, closest_enemy))
            elif zealot.health/zealot.health_max < 0.4:
                self.actions_list.append(move(zealot, (23, 16)))
            else:
                self.actions_list.append(attack(zealot, closest_enemy))

        if len(enemy_units) < 4 or len([eu for eu in enemy_units if eu.health/eu.health_max < 0.2]) > 2:
            for unit in units:
                self.actions_list.append(attack(unit, center(enemy_units)))

        return self.actions_list

