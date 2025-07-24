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
        

        if not agents or not enemies:
            return []

        # Stalker attack zealot first
        if enemy_zealots:
            target = nearest_n_units(center(agents), enemy_zealots, 1)[0]
        elif enemy_stalkers:
            target = nearest_n_units(center(agents), enemy_stalkers, 1)[0]
        else:
            target = center(enemies)

        for stalker in stalkers:
            if stalker.health/stalker.health_max < 0.5:
                # Retreat to starting point
                self.actions_list.append(move(stalker, (23, 16)))
            else:
                self.actions_list.append(attack(stalker, target, visible_matrix))

        target = nearest_n_units(center(agents), enemies, 1)[0]
        for zealot in zealots:
            if zealot.health/zealot.health_max < 0.5:
                self.actions_list.append(move(zealot, (23, 16)))
            else:
                self.actions_list.append(attack(zealot, target, visible_matrix))
            
        return self.actions_list

