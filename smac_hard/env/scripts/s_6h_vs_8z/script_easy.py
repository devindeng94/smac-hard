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
        
        
        
    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):


        self.units = [agent for _, agent in agents.items() if agent.health != 0]
        self.enemy_units = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        self.zealots = sorted([a for a in self.units if a.unit_type==UnitTypeId.ZEALOT.value], key=lambda a: a.tag)
        self.enemy_hydralisk = sorted([a for a in self.enemy_units if a.unit_type==UnitTypeId.HYDRALISK.value], key=lambda a: a.tag)

        if not self.units or not self.enemy_units:
            return []

        actions_list = []

        # Tacktic 1: Focus fire on one enemy
        if not self.enemy_hydralisk:
            return []
        
        for zealot in self.zealots:
            target = min(self.enemy_hydralisk, key=lambda e: distance_to(e, zealot))
            actions_list.append(attack(zealot, (target.pos.x, target.pos.y), visible_matrix))

        return actions_list