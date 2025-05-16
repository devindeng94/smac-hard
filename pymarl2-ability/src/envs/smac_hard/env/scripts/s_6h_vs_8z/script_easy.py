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
        
        
        
    def script(self, obs, iteration):

        actions_list = []
        init_unit(obs, self)

        # Tacktic 1: Focus fire on one enemy
        if not self.enemy_hydralisk:
            return []
        
        for zealot in self.zealots:
            target = min(self.enemy_hydralisk, key=lambda e: distance_to(e, zealot))
            actions_list.append(attack(zealot, (target.pos.x, target.pos.y)))

        return actions_list