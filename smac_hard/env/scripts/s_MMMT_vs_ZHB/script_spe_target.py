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

        # Spread out units in the early game to avoid tank splash
        if iteration < 10:
            self.spread_out_units(self.zerglings, 2)
            self.spread_out_units(self.hydralisks, 2)
            self.spread_out_units(self.banelings, 2)

        # Banelings → Marines
        for baneling in self.banelings:
            if self.enemy_marines:
                target = min(self.enemy_marines, key=lambda e: distance_to(e, baneling))
                self.actions_list.append(attack(baneling, target, visible_matrix))

        # Zerglings → Marauders (or anything if no Marauders)
        for zergling in self.zerglings:
            if self.enemy_marauders:
                target = min(self.enemy_marauders, key=lambda e: distance_to(zergling, e))
                
            else:
                target = min(enemies, key=lambda e: distance_to(zergling, e))
            
            self.actions_list.append(attack(zergling, target, visible_matrix))

        # Hydralisks → Siege Tank first, then Medivacs, then cleanup
        for hydralisk in self.hydralisks:
            if self.enemy_tanks:
                target = min(self.enemy_tanks, key=lambda e: distance_to(hydralisk, e))
            elif self.enemy_medivacs:
                target = min(self.enemy_medivacs, key=lambda e: distance_to(hydralisk, e))
            elif enemies:
                target = min(enemies, key=lambda e: distance_to(hydralisk, e))

            self.actions_list.append(attack(hydralisk, target, visible_matrix))

        return [a for a in self.actions_list if a != None]
    

    def spread_out_units(self, units, radius=2.0):
        for i, unit in enumerate(units):
            angle = i * (2 * math.pi / len(units))
            offset = (math.cos(angle) * radius, math.sin(angle) * radius)
            self.actions_list.append(move(unit, (unit.pos.x + offset[0], unit.pos.y+offset[1])))