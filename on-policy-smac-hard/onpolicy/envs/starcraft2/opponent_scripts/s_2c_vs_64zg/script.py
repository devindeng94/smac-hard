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
        
        self.enemy_colossuses = []
        self.enemy_list = ['enemy_colossuses']
        self.group_tags = {}
        
        self.positions = {
            'up_left': [(3.5, 14), (2, 16.5)],
            'up_right': [(26.5, 14), (28, 16.5),],
            'down_left': [(3.5, 6), (2.5, 10)],
            'down_right': [(26.5, 6), (27.5, 10)],
        }
        
        self.clif_y = 12
        self.up_group = ['up_left', 'up_right']
        self.down_group = ['down_left', 'down_right']
        
    def script(self, obs, iteration):
        
        actions_list = []
        init_unit(obs, self)

        
        group_units, group_centers = self.group()
        if self.switch_group(group_units['up_left'], group_units['down_left'], 'left') or self.switch_group(group_units['up_right'], group_units['down_right'], 'right'):
            group_units, group_centers = self.group()
        
        if iteration < 10:
            for group_id, group in group_units.items():
                pos = self.positions[group_id][0]
                for unit in group:
                    actions_list.append(move(unit, pos))
            # print(group_centers)
            return actions_list
        self.check_state()
        if self.attack_above:
            for group_id in self.up_group:
                group = group_units[group_id]
                center = group_centers[group_id]
                target_enemy = nearest_n_units(center, self.attack_above, 1)[0]
                for unit in group:
                    actions_list.append(attack(unit, target_enemy))
        else:
            for group_id in self.up_group:
                group = group_units[group_id]
                pos = self.positions[group_id][1]
                for unit in group:
                    actions_list.append(move(unit, pos))
        if self.attack_down:
            for group_id in self.down_group:
                group = group_units[group_id]
                center = group_centers[group_id]
                target_enemy = nearest_n_units(center, self.attack_down, 1)[0]
                for unit in group:
                    actions_list.append(attack(unit, target_enemy))
        else:
            for group_id in self.down_group:
                group = group_units[group_id]
                pos = self.positions[group_id][1]
                for unit in group:
                    actions_list.append(move(unit, pos))
        
        return actions_list
    
    
    def group(self):
        if not self.group_tags:
            self._group()
        unit_tags = [unit.tag for unit in self.zerglings ]
        group_units = {}
        for key, tags in self.group_tags.items():
            units, del_list = [], []
            for tag in tags:
                if tag in unit_tags:
                    tag_idx = unit_tags.index(tag)
                    units.append(self.zerglings[tag_idx])
                else:
                    del_list.append(tag)
            for tag in del_list:
                tags.remove(tag)
            group_units[key] = units
        group_centers = {}
        for key, group in group_units.items():
            group_centers[key] = (center(group) if group else (1000,1000))
        return group_units, group_centers
            
            
    def _group(self):
        self.group_tags = {
            'up_left':[],
            'up_right':[],
            'down_left':[],
            'down_right':[]
        }
        for unit in self.zerglings:
            if (unit.pos.x < 15.6 and unit.pos.y > 7.9) or (unit.pos.x < 16.3 and unit.pos.y > 10.1):
                self.group_tags['up_left'].append(unit.tag)
            elif (unit.pos.x > 16.3 and unit.pos.y > 7.9) or unit.pos.y > 8.6:
                self.group_tags['up_right'].append(unit.tag)
            elif (unit.pos.x > 15.6 and unit.pos.y < 7.2) or unit.pos.x > 16.3:
                self.group_tags['down_right'].append(unit.tag)
            else:
                self.group_tags['down_left'].append(unit.tag)
                
    def check_state(self):
        self.attack_above = [u for u in self.enemy_colossuses if u.pos.y > 11.9]
        self.attack_down = [u for u in self.enemy_colossuses if u.pos.y < 12.1]
        
    def switch_group(self, g1, g2, key):
        if len(g1) > len(g2) * 2 + 2:
            n = (len(g1) - len(g2) * 2 - 1)//2
            switch_list = sorted(g1, key=lambda e: e.pos.y)[:n]
            for unit in switch_list:
                self.group_tags['up_'+key].remove(unit.tag)
                self.group_tags['down_'+key].append(unit.tag)
            return True
        elif len(g1) < len(g2) * 2 - 2:
            n = (len(g2) * 2 - 1 - len(g1))//2
            switch_list = sorted(g2, key=lambda e: e.pos.y)[:n]
            for unit in switch_list:
                self.group_tags['down_'+key].remove(unit.tag)
                self.group_tags['up_'+key].append(unit.tag)
            return True
        
        return False