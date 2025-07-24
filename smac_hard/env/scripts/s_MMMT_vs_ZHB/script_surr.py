import math
import random
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        self.map_name = map_name
        self.init = True
        self.engage = True
        self.center = None
        
    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):


        agents = [agent for _, agent in agents.items() if agent.health != 0]
        enemies = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        if not agents or not enemies:
            return
        
        self.banelings = sorted([a for a in agents if a.unit_type==UnitTypeId.BANELING.value], key=lambda a: a.tag)
        self.hydralisks = sorted([a for a in agents if a.unit_type==UnitTypeId.HYDRALISK.value], key=lambda a: a.tag)
        self.zerglings = sorted([a for a in agents if a.unit_type==UnitTypeId.ZERGLING.value], key=lambda a: a.tag)

        self.enemy_marines = sorted([a for a in enemies if a.unit_type==UnitTypeId.MARINE.value], key=lambda a: a.tag)
        self.enemy_marauders = sorted([a for a in enemies if a.unit_type==UnitTypeId.MARAUDER.value], key=lambda a: a.tag)
        self.enemy_medivacs = sorted([a for a in enemies if a.unit_type==UnitTypeId.MEDIVAC.value], key=lambda a: a.tag)
        self.enemy_tanks = sorted([a for a in enemies if a.unit_type==UnitTypeId.SIEGETANK.value or a.unit_type==UnitTypeId.SIEGETANKSIEGED.value], key=lambda a: a.tag)

        self.actions_list = []

        # Target center of mass for flanking
        if enemies:
            enemy_center = center(enemies)

            # Zerglings: Split to flank
            left_flank = self.zerglings[:len(self.zerglings)//2]
            right_flank = self.zerglings[len(self.zerglings)//2:]

            for i, lz in enumerate(left_flank):
                offset = (-3, 2 + i % 3)
                self.actions_list.append(attack(lz, (enemy_center[0]+offset[0], enemy_center[1]+offset[1]), visible_matrix))

            for i, rz in enumerate(right_flank):
                offset = (3, -2 - i % 3)
                self.actions_list.append(attack(rz, (enemy_center[0]+offset[0], enemy_center[1]+offset[1]), visible_matrix))

            # Banelings: Approach from back
            for baneling in self.banelings:
                if self.enemy_marines:
                    target = min(self.enemy_marines, key=lambda e: distance_to(baneling, e))
                else:
                    target = min(enemies, key=lambda e: distance_to(baneling, e))
                # Offset to come from behind the target
                backdoor = toward(target, (29, 16), -5)
                self.actions_list.append(attack(baneling, backdoor, visible_matrix))

            # Hydralisks: Target Siege Tank, Medivac, or safest visible enemy
            for hydralisk in self.hydralisks:
                if self.enemy_tanks:
                    target = min(self.enemy_tanks, key=lambda e: distance_to(e, hydralisk))
                elif self.enemy_medivacs:
                    target = min(self.enemy_medivacs, key=lambda e: distance_to(e, hydralisk))
                elif enemies:
                    target = min(enemies, key=lambda e: distance_to(e, hydralisk))
                    
                self.actions_list.append(attack(hydralisk, target, visible_matrix))

        return [a for a in self.actions_list if a != None]
    