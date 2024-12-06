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
                
    def script(self, obs, iteration):

        actions_list = []
        init_unit(obs, self)

        # Tacktic 1: Focus fire on one enemy
        if not self.enemy_zealots or not self.zerglings:
            return []
        
        # Move to (13, 13) First
        if iteration < 10:
            for z in self.zerglings:
                actions_list.append(move(z, (13, 13)))
            return actions_list
        

        #target = min(self.enemy_zealots, key=lambda ez: distance_to(ez, center(self.zerglings)))

        for idx, z in enumerate(self.zerglings):
            
            target = min(nearest_n_units(z, self.enemy_zealots, 2), key=lambda ez: ez.health)
            actions_list.append(attack(z, target))

        return actions_list