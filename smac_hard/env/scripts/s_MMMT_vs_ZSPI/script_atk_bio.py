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
        self.start_position = (19, 16)
        self.enemy_position = (3, 16)
        
    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):


        agents = [agent for _, agent in agents.items() if agent.health != 0]
        enemies = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        if not agents or not enemies:
            return
        
        self.zealots = sorted([a for a in agents if a.unit_type==UnitTypeId.ZEALOT.value], key=lambda a: a.tag)
        self.stalkers = sorted([a for a in agents if a.unit_type==UnitTypeId.STALKER.value], key=lambda a: a.tag)
        self.immortals = sorted([a for a in agents if a.unit_type==UnitTypeId.IMMORTAL.value], key=lambda a: a.tag)
        self.phoenixes = sorted([a for a in agents if a.unit_type==UnitTypeId.PHOENIX.value], key=lambda a: a.tag)

        self.enemy_marines = sorted([a for a in enemies if a.unit_type==UnitTypeId.MARINE.value], key=lambda a: a.tag)
        self.enemy_marauders = sorted([a for a in enemies if a.unit_type==UnitTypeId.MARAUDER.value], key=lambda a: a.tag)
        self.enemy_medivacs = sorted([a for a in enemies if a.unit_type==UnitTypeId.MEDIVAC.value], key=lambda a: a.tag)
        self.enemy_tanks = sorted([a for a in enemies if a.unit_type==UnitTypeId.SIEGETANK.value or a.unit_type==UnitTypeId.SIEGETANKSIEGED.value], key=lambda a: a.tag)

        self.actions_list = []


        
        for phoenix in self.phoenixes:
            if phoenix.energy >= 50 and self.enemy_tanks:
                # 173 GRAVITONBEAM
                target = min(self.enemy_tanks, key=lambda t: distance_to(t, phoenix))
                if distance_to(phoenix, target) < 10:
                    self.actions_list.append(apply_ability(phoenix, 173, target))
                else:
                    self.actions_list.append(move(phoenix, target))
            else:
                target = min(enemies, key=lambda m: distance_to(phoenix, m))
                self.actions_list.append(attack(phoenix, target, visible_matrix))


        bio = self.enemy_marauders + self.enemy_marines
        for zealot in self.zealots:
            if bio:
                target = min(bio, key=lambda b: distance_to(b, zealot))
                self.actions_list.append(attack(zealot, target, visible_matrix))

        targets = self.enemy_marauders + self.enemy_tanks
        for immortal in self.immortals:
            if targets:
                target = min(targets, key=lambda t: distance_to(t, immortal))
                self.actions_list.append(attack(immortal, target, visible_matrix))

        medivacs = self.enemy_medivacs
        for stalker in self.stalkers:
            if medivacs:
                target = min(medivacs, key=lambda m: distance_to(stalker, m))
            elif bio:
                target = min(bio, key=lambda b: distance_to(stalker, b))
            else:
                continue

            self.actions_list.append(attack(stalker, target, visible_matrix))
        
        return self.actions_list