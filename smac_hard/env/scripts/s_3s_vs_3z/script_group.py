import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name
        self.init = True
        self.target_dict = {}

    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):


        self.units = [agent for _, agent in agents.items() if agent.health != 0]
        self.enemy_units = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        zealots = sorted([a for a in self.units if a.unit_type==UnitTypeId.ZEALOT.value], key=lambda a: a.tag)
        enemy_stalkers = sorted([a for a in self.enemy_units if a.unit_type==UnitTypeId.STALKER.value], key=lambda a: a.tag)

        self.actions_list = []

        if not self.units or not self.enemy_units:
            return []
        
        if self.init:
            for i, zealot in enumerate(zealots):
                self.target_dict[zealot.tag] = enemy_stalkers[i%len(enemy_stalkers)]
            self.init = False


        if not zealots or not enemy_stalkers:
            return []
        
        
        # Allocate zealots to groups
        for i, z in enumerate(zealots):
            target = self.target_dict[z.tag]
            if target.health == 0:
                target = nearest_n_units(z, enemy_stalkers, 1)[0]
                self.target_dict[z.tag] = target

            self.actions_list.append(attack(z, target, visible_matrix))

        return self.actions_list

    
        