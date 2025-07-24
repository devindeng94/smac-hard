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
        
        self.zealots = []
        self.ally_list = ['zealots']
        
        self.enemy_hydralisk = []
        self.enemy_list = ['enemy_hydralisk']
        
        self.target = {}
        self.init = True
        
        
        
    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):


        self.units = [agent for _, agent in agents.items() if agent.health != 0]
        self.enemy_units = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        self.zealots = sorted([a for a in self.units if a.unit_type==UnitTypeId.ZEALOT.value], key=lambda a: a.tag)
        self.enemy_hydralisk = sorted([a for a in self.enemy_units if a.unit_type==UnitTypeId.HYDRALISK.value], key=lambda a: a.tag)

        if not self.units or not self.enemy_units:
            return []

        actions_list = []

        
        if self.init:
            for i, zealot in enumerate(self.zealots):
                self.target[zealot.tag] = self.enemy_hydralisk[i % len(self.enemy_hydralisk)]
            self.init = False


        # Tacktic 1: Focus fire on one enemy
        if not self.enemy_hydralisk:
            return []
        

        for zealot in self.zealots:
            t = self.target[zealot.tag]
            if t.health==0:
                # Re-assign another target
                t = nearest_n_units(zealot, self.enemy_hydralisk, 1)[0]
                self.target[zealot.tag] = t
            actions_list.append(attack(zealot, t, visible_matrix))

        return actions_list