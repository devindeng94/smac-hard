import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId
from scipy.spatial.distance import pdist, squareform
import numpy as np

class DecisionTreeScript():

    def __init__(self, map_name):
        self.map_name = map_name
        
        self.target_dict = {}
                
    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):


        self.units = [agent for _, agent in agents.items() if agent.health != 0]
        self.enemy_units = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        self.zerglings = sorted([a for a in self.units if a.unit_type==UnitTypeId.ZERGLING.value], key=lambda a: a.tag)
        self.enemy_zealots = sorted([a for a in self.enemy_units if a.unit_type==UnitTypeId.ZEALOT.value], key=lambda a: a.tag)

        if not self.units or not self.enemy_units:
            return []

        actions_list = []


        # Tacktic 1: Focus fire on one enemy
        if not self.enemy_zealots or not self.zerglings:
            return []
        
        # Assign target to each agent
        if distance_to(center(self.enemy_zealots), center(self.zerglings)) > 3:
            for i, z in enumerate(self.zerglings):
                self.target_dict[z.tag] = self.enemy_zealots[i % len(self.enemy_zealots)]
                actions_list.append(move(z, center(self.enemy_zealots)))
            return actions_list
        
        else:

            for i, z in enumerate(self.zerglings):
                target = self.target_dict[z.tag]
                if target.health == 0:
                    target = nearest_n_units(z, self.enemy_zealots, 1)[0]
                
                actions_list.append(attack(z, (target.pos.x, target.pos.y), visible_matrix))
                self.target_dict[z.tag] = target

        return actions_list