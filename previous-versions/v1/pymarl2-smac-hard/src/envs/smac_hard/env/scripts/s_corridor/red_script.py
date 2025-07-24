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
        self.ally_list = ['enemy_zerglings']
        
        self.zealots = []
        self.enemy_list = ['zealots']
                
    def script(self, obs, iteration):

        actions_list = []
        init_unit(obs, self)

        retreat_position = (11, 11)

        # Tacktic 1: Focus fire on one enemy
        if not self.zealots or not self.enemy_zerglings:
            return []
        
        spread_positions = [
            (12, 13), (13, 13), (11, 13),
            (12, 14), (12, 12), (13, 14)
        ]

        for i, zealot in enumerate(self.zealots):

            if distance_to(zealot, spread_positions[i]) > 2:
                actions_list.append(move(zealot, spread_positions[i]))
                continue

            nearest_zergling = nearest_n_units(zealot, self.enemy_zerglings, 1)[0]
            if nearest_zergling and zealot.weapon_cooldown == 0:
                actions_list.append(attack(zealot, nearest_zergling))

            else:
                if zealot.health < 25:
                    actions_list.append(move(zealot, retreat_position))
                else:
                    actions_list.append(move(zealot, nearest_zergling))
        
        return actions_list