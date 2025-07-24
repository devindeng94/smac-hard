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

    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):
        
        # Change from dict to list
        agents = [agent for _, agent in agents.items() if agent.health != 0]
        enemies = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        self.actions_list = []


        stalkers = [unit for unit in agents if unit.unit_type==UnitTypeId.STALKER.value]
        zealots = [unit for unit in agents if unit.unit_type==UnitTypeId.ZEALOT.value]

        enemy_zealots = sorted([unit for unit in enemies if unit.unit_type==UnitTypeId.STALKER.value], key=lambda u:u.tag)
        enemy_stalkers = sorted([unit for unit in enemies if unit.unit_type==UnitTypeId.STALKER.value], key=lambda u:u.tag)


        for stalker in stalkers:
            closest_enemy = nearest_n_units(stalker, enemies, 1)[0]

            if distance_to(stalker, closest_enemy) > SHOOT_RANGE:
                self.actions_list.append(attack(stalker, closest_enemy, visible_matrix))
            elif stalker.health/stalker.health_max < 0.5:
                self.actions_list.append(move(stalker, (23, 16)))
            else:
                self.actions_list.append(attack(stalker, closest_enemy, visible_matrix))

        for zealot in zealots:
            closest_enemy = nearest_n_units(zealot, enemies, 1)[0]

            if distance_to(zealot, closest_enemy) > 0.1:
                self.actions_list.append(attack(zealot, closest_enemy, visible_matrix))
            elif zealot.health/zealot.health_max < 0.4:
                self.actions_list.append(move(zealot, (23, 16)))
            else:
                self.actions_list.append(attack(zealot, closest_enemy, visible_matrix))

        if len(enemies) < 4 or len([eu for eu in enemies if eu.health/eu.health_max < 0.2]) > 2:
            for unit in agents:
                self.actions_list.append(attack(unit, center(enemies), visible_matrix))

        return self.actions_list

