import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId
import numpy as np

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name
        self.zealots = []
        self.ally_list = ['zealots']
        
        self.enemy_stalkers = []
        self.enemy_list = ['enemy_stalkers']
        
        self.pos_init = True
        self.stage = 0
        self.zealots_tags = []
        self.center_distance = 13
        

    def script(self, obs, iteration):
        
        actions_list = []
        init_unit(obs, self)
        self.sort_zealots()
        self.zealots = sorted([unit for unit in self.zealots], key=lambda u: u.tag)
        # x1 = [u.pos.x for u in self.zealots]
        # y1 = [u.pos.y for u in self.zealots]
        # x2 = [u.pos.x for u in self.enemy_stalkers]
        # y2 = [u.pos.y for u in self.enemy_stalkers]
        # print(x1, y1)
        # import matplotlib.pyplot as plt
        
        # plt.scatter(x1, y1, c='b')
        # plt.scatter(x2, y2, c='r')
        # ax = plt.gca()
        # ax.set_aspect(1)
        # plt.show()
        if self.pos_init and self.close_check():
            target_center = self.get_target_center()
            agent_pos_center = center(self.zealots)
            agent_center = self.get_agent_center(target_center, agent_pos_center)
            
            pos_list = self.get_pos_list(agent_center)
            if self.pos_init:
                for p, u in zip(pos_list, self.zealots):
                    actions_list.append(move(u, p))
                return actions_list
            
        for z in self.zealots:
            target = nearest_n_units(z, self.enemy_stalkers, 1)[0]
            actions_list.append(attack(z, target))
        


        return actions_list

    def sort_zealots(self):
        if not self.zealots_tags:
            x = [u.pos.x for u in self.zealots]
            y = [u.pos.y for u in self.zealots]
            self.zealots_tags.append(self.zealots[np.argmax(x)].tag)
            self.zealots_tags.append(self.zealots[np.argmax(y)].tag)
            self.zealots_tags.append(self.zealots[np.argmin(y)].tag)
            for z in self.zealots:
                if z.tag not in self.zealots_tags:
                    self.zealots_tags.append(z.tag)
                    break
        zealots = []
        for t in self.zealots_tags:
            for z in self.zealots:
                if z.tag == t:
                    zealots.append(z)
                    break
        self.zealots = zealots
    
    def close_check(self):
        for z in self.zealots:
            if distance_to(z, nearest_n_units(z, self.enemy_stalkers, 1)[0]) < 6.5:
                self.pos_init = False
                return False
        return True
    
    def get_target_center(self):
        target_center = center(self.enemy_stalkers)
        for s in self.enemy_stalkers:
            if distance_to(s, target_center) > 3:
                target_center = None
                break
        if target_center is not None:
            return target_center
        agent_center = center(self.zealots)
        closest_enemy = nearest_n_units(agent_center, self.enemy_stalkers, 1)[0]
        return (closest_enemy.pos.x, closest_enemy.pos.y)
            
    def get_agent_center(self, target_center, center_pos):
        if self.stage > 0:
            self.center_distance = 8
            return toward(target_center, center_pos, self.center_distance)
        if distance_to(target_center, center_pos) > self.center_distance:
            return center_pos
        return toward(target_center, center_pos, self.center_distance)
    
    def _pos_list(self, x, y, stage):
        pos_list = [
            [
                (x, y+2),
                (x, y+4),
                (x, y-4),
                (x, y-2),
            ],[
                (x-8+4*math.sqrt(3), y+4),
                (x-8, y+8),
                (x-8, y-8),
                (x-8+4*math.sqrt(3), y-4),
            ],[
                (x-8+4*math.sqrt(3), y+4),
                (x-8-4*math.sqrt(3), y+4),
                (x-8-4*math.sqrt(3), y-4),
                (x-8+4*math.sqrt(3), y-4),
            ]
        ]
        return pos_list[stage]

    def check_pos_list(self, pos_list):
        for p, u in zip(pos_list, self.zealots):
            if distance_to(p, u) > 1:
                return False
        return True
        
    def get_pos_list(self, agent_center):
        x, y = agent_center
        while self.stage < 3:
            pos_list = self._pos_list(x, y, self.stage)
            if self.check_pos_list(pos_list):
                self.stage += 1
            else:
                return pos_list
        self.pos_init = False
        return []