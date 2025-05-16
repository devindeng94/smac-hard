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
        
        self.enemy_zerglings = []
        self.enemy_banelings = []
        self.ally_list = ['enemy_banelings', 'enemy_zerglings']
        
        self.banelings = []
        self.zerglings = []
        self.enemy_list = ['banelings', 'zerglings']
                
    def script(self, obs, iteration):

        actions_list = []
        init_unit(obs, self)

        enemies = self.enemy_banelings + self.enemy_zerglings

        if not self.enemy_banelings and not self.enemy_zerglings:
            return

        groups = [[], []]
        for i, baneling in enumerate(self.banelings):
            groups[i%2].append(baneling)
        
        for i, zergling in enumerate(self.zerglings):
            groups[i%2].append(zergling)


        for u in groups[0]:
            if self.enemy_zerglings:
                actions_list.append(attack(u, center(self.enemy_zerglings)))
            else:
                actions_list.append(attack(u, center(self.enemy_banelings)))

        if groups[1]:
            if distance_to(center(groups[1]), (16, 8)) < 2:
                for u in groups[1]:
                    target = min(enemies, key=lambda e: distance_to(e, u))
                    actions_list.append(attack(u, target))

            else:
                for u in groups[1]:
                    actions_list.append(move(u, (16, 8)))
        
        return actions_list