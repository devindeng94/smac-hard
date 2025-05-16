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
        
        self.zerglings = []
        self.ally_list = ['zerglings']
        
        self.enemy_zealots = []
        self.enemy_list = ['enemy_zealots']
        self.target_dict = {}
                
    def script(self, obs, iteration):

        actions_list = []
        init_unit(obs, self)
        self.zerglings = sorted(self.zerglings, key=lambda u: u.tag)
        self.enemy_zealots = sorted(self.enemy_zealots, key=lambda e: e.tag)


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
                if not target.is_active:
                    target = nearest_n_units(z, self.enemy_zealots, 1)[0]
                
                actions_list.append(attack(z, (target.pos.x, target.pos.y)))
                self.target_dict[z.tag] = target

        return actions_list