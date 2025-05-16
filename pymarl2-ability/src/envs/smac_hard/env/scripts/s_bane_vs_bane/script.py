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
        self.banelings = []
        self.ally_list = ['banelings', 'zerglings']
        
        self.enemy_banelings = []
        self.enemy_zerglings = []
        self.enemy_list = ['enemy_banelings', 'enemy_zerglings']
        self.radius = 10 
        self.center = (16, 21)

    def script(self, obs, iteration):

        actions_list = []
        init_unit(obs, self)

        enemy_units = self.enemy_banelings + self.enemy_zerglings

        if not enemy_units:
            return []

        # Baneling attack zerglings.
        for baneling in self.banelings:
            target = self.find_best_attack_target(self.enemy_zerglings)
            if target == None:
                target = self.find_best_attack_target(enemy_units)
            actions_list.append(attack(baneling, target))

        # Zergling spread out.
        if iteration < 10:
            
            for i, zergling in enumerate(self.zerglings):

                angle = math.pi / len(self.zerglings) * i
                delta_x = math.cos(angle)
                delta_y = math.sin(angle)
                actions_list.append(move(zergling, (delta_x*self.radius + self.center[0], delta_y*self.radius+self.center[1])))
            return actions_list            

        for zergling in self.zerglings:

            target = min(enemy_units, key=lambda eu: distance_to(eu, zergling))
            actions_list.append(attack(zergling, target))

        return actions_list
    
        
    

    def find_best_attack_target(self, enemies):

        best_target = None
        highest_density = -1

        for enemy in enemies:
            nearby_enemies = closer_than(enemy, enemies, 2)
            if len(nearby_enemies) > highest_density:
                highest_density = len(nearby_enemies)
                best_target = enemy

        return best_target