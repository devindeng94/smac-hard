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
        
        self.banelings = []
        self.ally_list = ['banelings']
        
        self.enemy_zealots = []
        self.enemy_list = ['enemy_zealots']
        
        self.group_tags = []
        
        self.init_position = [
            (19, 27),
            (23, 23),
            (27, 19), 
            (23, 31),
            (27, 27),
            (31, 23),
            (31, 31),
        ]
        self.init_steps = 5
        
    def script(self, obs, iteration):

        actions_list = []
        init_unit(obs, self)
        group_units, group_centers = self.group()
        if iteration < self.init_steps:
            for group, pos in zip(group_units, self.init_position):
                for unit in group:
                    actions_list.append(move(unit, pos))
            return actions_list
        
        final = self.check_final(iteration)
        
        close_enemy_pair = self.get_close_enemy_pairs()
        attack_close_groups = self.get_attack_close_group(close_enemy_pair, group_centers)
        
        for group_id, enemy_pair in zip(attack_close_groups, close_enemy_pair[:len(attack_close_groups)]):
            enemy_x = self.enemy_zealots[enemy_pair[0]]
            enemy_y = self.enemy_zealots[enemy_pair[1]]
            pair_center = ((enemy_x.pos.x+enemy_y.pos.x)/2, (enemy_x.pos.y+enemy_y.pos.y)/2)
            enemy_x_hp = enemy_x.health+enemy_x.shield
            enemy_y_hp = enemy_y.health+enemy_y.shield
            for unit in group_units[group_id]:
                if max(enemy_x_hp, enemy_y_hp) < 0:
                    self.add_to_group(unit, group_id, group_centers, iteration)
                    continue
                dis_x = distance_to(unit, enemy_x)
                dis_y = distance_to(unit, enemy_y)
                if max(dis_x, dis_y) < 2:
                    actions_list.append(attack(unit, enemy_x))
                    enemy_x_hp -= 35
                    enemy_y_hp -= 35
                else:
                    actions_list.append(move(unit, pair_center))
        if final:
            rest_enemy = list(range(len(self.enemy_zealots)))
            for p in close_enemy_pair:
                rest_enemy.remove(p[0])
                rest_enemy.remove(p[1])
            rest_group = [i for i in range(len(group_units)) if (i not in attack_close_groups and group_units[i])]
            while rest_enemy and rest_group:
                enemy_id = rest_enemy.pop(0)
                enemy = self.enemy_zealots[enemy_id]
                rest_center = [group_centers[i] for i in rest_group]
                group_id = rest_group.pop(np.argmin([distance_to(enemy, rc) for rc in rest_center]))
                group = group_units[group_id]
                enemy_hp = enemy.health + enemy.shield
                for unit in group:
                    if enemy_hp < 0:
                        self.add_to_group(unit, group_id, group_centers, iteration)
                        continue
                    dis = distance_to(unit, enemy)
                    if dis < 2:
                        actions_list.append(attack(unit, enemy))
                        enemy_hp -= 35
                    else:
                        actions_list.append(move(unit, enemy))
                
        else:
            for i, (group, pos) in enumerate(zip(group_units, self.init_position)):
                if i in attack_close_groups:
                    continue
                d = (iteration - self.init_steps) // 2
                target_pos = (pos[0]-d, pos[1]-d)
                for unit in group:
                    actions_list.append(move(unit, target_pos))
            
        return actions_list
        
        
        # zealots = sorted([unit for unit in obs.observation.raw_data.units if unit.owner==1], key=lambda u: u.tag)
        # banelings = sorted([unit for unit in obs.observation.raw_data.units if unit.owner==2], key=lambda u: u.tag)
        # print(banelings[0].pos.x, banelings[0].pos.y)
        # print(banelings[0].orders)
        # return [attack(banelings[0], zealots[0])]

    def group(self):
        if not self.group_tags:
            self._group()
        unit_tags = [unit.tag for unit in self.banelings ]
        group_units = []
        for tags in self.group_tags:
            units, del_list = [], []
            for tag in tags:
                if tag in unit_tags:
                    tag_idx = unit_tags.index(tag)
                    units.append(self.banelings[tag_idx])
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
        tags = [unit.tag for unit in self.banelings]
        poses = [(unit.pos.x, unit.pos.y) for unit in self.banelings]
        for p in self.init_position[:6]:
            self.group_tags.append([])
            dis = [distance_to(p, tp) for tp in poses]
            closet_id = sorted(np.argsort(dis).tolist()[:5], reverse=True)
            for id in closet_id:
                self.group_tags[-1].append(tags[id])
                tags.pop(id)
                poses.pop(id)
        self.group_tags.append(tags)
        
    def get_close_enemy_pairs(self):
        
        poses = [[unit.pos.x, unit.pos.y] for unit in self.enemy_zealots]
        distance = squareform(pdist(poses, metric='euclidean'))
        for i in range(len(poses)):
            distance[i, i] = 1000
        close_enemy_pair = []
        while np.min(distance) < 2:
            min_i = int(np.argmin(distance))
            x, y = min_i//len(poses), min_i%len(poses)
            distance[:, x] = 1000
            distance[x, :] = 1000
            distance[y, :] = 1000
            distance[:, y] = 1000
            close_enemy_pair.append([x, y])
        return close_enemy_pair

    def get_attack_close_group(self, close_enemy_pair, group_centers):
        attack_close_groups = []
        for pair in close_enemy_pair:
            en_x, en_y = self.enemy_zealots[pair[0]], self.enemy_zealots[pair[1]]
            pair_center = ((en_x.pos.x+en_y.pos.x)/2, (en_x.pos.y+en_y.pos.y)/2)
            dis_list = [distance_to(pair_center, c) for c in group_centers]
            if min(dis_list) > 100:
                break
            closest_group_id = np.argmin(dis_list)
            group_centers[closest_group_id] = (1000, 1000)
            attack_close_groups.append(closest_group_id)
        return attack_close_groups
    
    def add_to_group(self, unit, group_id, group_centers, iteration):
        less_groups, empty_groups = [], []
        for i, group in enumerate(self.group_tags):
            if i == group_id:
                continue
            if len(group) == 0:
                empty_groups.append(i)
            elif len(group) < 5:
                less_groups.append(i)
                
        if less_groups:
            target_pos = [group_centers[g] for g in less_groups]
            target_id = less_groups[np.argmin([distance_to(unit, p) for p in target_pos])]
        elif empty_groups:
            d = (iteration - self.init_steps) // 2
            target_pos = [(self.init_position[g][0]-d, self.init_position[g][1]-d) for g in empty_groups]
            target_id = empty_groups[np.argmin([distance_to(unit, p) for p in target_pos])]
        self.group_tags[group_id].remove(unit.tag)
        self.group_tags[target_id].append(unit.tag)
        
    def check_final(self, iteration):
        farthest_enemy = min([min(u.pos.x, u.pos.y) for u in self.enemy_zealots])
        farthest_ally = 19 - (iteration - self.init_steps) // 2
        if farthest_ally <= farthest_enemy or farthest_ally < 2:
            return True
        return False