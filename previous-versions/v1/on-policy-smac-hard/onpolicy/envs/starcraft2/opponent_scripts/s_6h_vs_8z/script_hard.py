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
        
        
        
    def script(self, obs, iteration):

        actions_list = []
        init_unit(obs, self)

        
        if self.init:
            for i, zealot in enumerate(self.zealots):
                self.target[zealot.tag] = self.enemy_hydralisk[i % len(self.enemy_hydralisk)]
            self.init = False


        # Tacktic 1: Focus fire on one enemy
        if not self.enemy_hydralisk:
            return []
        

        for zealot in self.zealots:
            t = self.target[zealot.tag]
            if not t.is_active:
                # Re-assign another target
                t = nearest_n_units(zealot, self.enemy_hydralisk, 1)[0]
                self.target[zealot.tag] = t
            actions_list.append(attack(zealot, t))

        return actions_list