import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        self.map_name = map_name
        
        self.spine_crawlers = []
        self.ally_list = ['spine_crawlers']
        
        self.enemy_stalkers = []
        self.enemy_list = ['enemy_stalkers']
        
        self.attack_range = 8.7
        
    def script(self, obs, iteration):

        actions_list = []
        init_unit(obs, self)
        spine_crawler = self.spine_crawlers[0]

        if not self.enemy_stalkers:
            return []

        if len(self.enemy_stalkers) == 1:
            target_enemy = self.enemy_stalkers[0]
        else:
            dis_0 = distance_to(spine_crawler, self.enemy_stalkers[0])
            dis_1 = distance_to(spine_crawler, self.enemy_stalkers[1])
            if dis_0 < self.attack_range and dis_1 < self.attack_range:
                if self.enemy_stalkers[0].health == self.enemy_stalkers[1].health:
                    target_enemy = nearest_n_units(spine_crawler, self.enemy_stalkers, 1)[0]
                else:
                    target_enemy = self.enemy_stalkers[0] if self.enemy_stalkers[0].health < self.enemy_stalkers[1].health else self.enemy_stalkers[1]
                actions_list.append(attack(spine_crawler, target_enemy))
            elif dis_0 < self.attack_range:
                actions_list.append(attack(spine_crawler, self.enemy_stalkers[0]))
            elif dis_1 < self.attack_range:
                actions_list.append(attack(spine_crawler, self.enemy_stalkers[1]))
        return actions_list
