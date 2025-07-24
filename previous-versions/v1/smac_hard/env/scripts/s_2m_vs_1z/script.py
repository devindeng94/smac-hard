import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        self.map_name = map_name
        
        self.zealots = []
        self.ally_list = ['zealots']
        
        self.enemy_marines = []
        self.enemy_list = ['enemy_marines']
        
    def script(self, obs, iteration):

        actions_list = []
        init_unit(obs, self)
        zealot = self.zealots[0]

        if not self.enemy_marines:
            return []

        if len(self.enemy_marines) == 1:
            target_enemy = self.enemy_marines[0]
        else:
            if self.enemy_marines[0].health == self.enemy_marines[1].health:
                target_enemy = nearest_n_units(zealot, self.enemy_marines, 1)[0]
            else:
                target_enemy = self.enemy_marines[0] if self.enemy_marines[0].health < self.enemy_marines[1].health else self.enemy_marines[1]
        actions_list.append(attack(zealot, target_enemy))
        return actions_list
