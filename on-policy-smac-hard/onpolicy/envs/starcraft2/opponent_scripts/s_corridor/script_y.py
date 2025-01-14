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
        self.group_tags = []
        self.init_position = [(15, 22), (22, 15)]
        self.start_tag = True
                
    def script(self, obs, iteration):

        actions_list = []
        init_unit(obs, self)
        group_units, group_centers = self.group()
        if iteration < 13 and self.start_tag and self.check_start(group_centers):
            for group, pos in zip(group_units, self.init_position):
                for unit in group:
                    actions_list.append(move(unit, pos))
            # print(group_centers)
            return actions_list
        # Tacktic 1: Focus fire on one enemy

        for idx, z in enumerate(self.zerglings):
            
            target = min(nearest_n_units(z, self.enemy_zealots, 2), key=lambda ez: ez.health)
            actions_list.append(attack(z, target))

        return actions_list
    
    def check_start(self, group_centers):
        poses = [(unit.pos.x, unit.pos.y) for unit in self.enemy_zealots]
        for pos in poses:
            if pos[0] > group_centers[0][0] and pos[1] > group_centers[1][1]:
                self.start_tag = False
                return False
        for g in group_centers:
            if distance_to(g, nearest_n_units(g, poses, 1)[0]) < 6:
                self.start_tag = False
                return False
        return True
    
    def group(self):
        if not self.group_tags:
            self._group()
        unit_tags = [unit.tag for unit in self.zerglings ]
        group_units = []
        for tags in self.group_tags:
            units, del_list = [], []
            for tag in tags:
                if tag in unit_tags:
                    tag_idx = unit_tags.index(tag)
                    units.append(self.zerglings[tag_idx])
                else:
                    del_list.append(tag)
            for tag in del_list:
                tags.remove(tag)
            group_units.append(units)
        group_centers = []
        for group in group_units:
            group_centers.append(center(group) if group else (1000,1000))
        return group_units, group_centers
            
            
    def _group(self):
        self.group_tags = [[], []]
        for unit in self.zerglings:
            if unit.pos.x > 28.25  or (unit.pos.x > 27.5 and unit.pos.y < 27.8):
                self.group_tags[0].append(unit.tag)
            else:
                self.group_tags[1].append(unit.tag)