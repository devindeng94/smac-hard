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


        # Phoenix Micro: Lift Siege Tanks and Medivacs first
        if self.phoenixes:
            targets = self.enemy_tanks

            for phoenix in self.phoenixes:
                if targets:
                    closest_target = min(targets, key=lambda t: distance_to(t, phoenix))
                    if distance_to(phoenix, closest_target) < 10:
                        # 173 GRAVITONBEAM
                        self.actions_list.append(apply_ability(phoenix, 173, closest_target))
                        targets.remove(closest_target)
                    else:
                        self.actions_list.append(attack(phoenix, closest_target, visible_matrix))
                else:
                    # If no high-priority targets, attack Marines
                    if enemies:
                        ph_target = min(enemies, key=lambda e: distance_to(e, phoenix))
                        self.actions_list.append(attack(phoenix, ph_target, visible_matrix))

        # Zealots: Charge into Marines to tank
        if self.zealots:
            if self.enemy_marines:
                for zealot in self.zealots:
                    self.actions_list.append(attack(zealot, center(self.enemy_marines), visible_matrix))
            else:
                for zealot in self.zealots:
                    self.actions_list.append(attack(zealot, center(enemies), visible_matrix))

        # Immortals: Focus Marauders first, then Medivacs
        if self.immortals:
            if self.enemy_marauders:
                for immortal in self.immortals:
                    im_target = min(self.enemy_marauders, key=lambda e: distance_to(e, immortal))
                    self.actions_list.append(attack(immortal, im_target, visible_matrix))
            elif self.enemy_medivacs:
                for immortal in self.immortals:
                    im_target = min(self.enemy_medivacs, key=lambda e: distance_to(e, immortal))
                    self.actions_list.append(attack(immortal, im_target, visible_matrix))
            else:
                for immortal in self.immortals:
                    im_target = min(enemies, key=lambda e: distance_to(e, immortal))
                    self.actions_list.append(attack(immortal, im_target, visible_matrix))

        # Stalkers: Focus Marauders/Medivacs, use Blink if low HP
        if self.stalkers:
            
            if self.enemy_marauders:
                for stalker in self.stalkers:
                    im_target = min(self.enemy_marauders, key=lambda e: distance_to(e, stalker))
                    self.actions_list.append(attack(stalker, im_target, visible_matrix))
            elif self.enemy_medivacs:
                for stalker in self.stalkers:
                    im_target = min(self.enemy_medivacs, key=lambda e: distance_to(e, stalker))
                    self.actions_list.append(attack(stalker, im_target, visible_matrix))
            else:
                for stalker in self.stalkers:
                    im_target = min(enemies, key=lambda e: distance_to(e, stalker))
                    self.actions_list.append(attack(stalker, im_target, visible_matrix))

            # Blink micro if health is low
            for stalker in self.stalkers:
                if stalker.health / stalker.health_max < 0.5:
                    retreat_pos = toward(self.start_position, stalker, -5)
                    # blink 3687
                    self.actions_list.append(apply_ability(stalker, 3687, retreat_pos))

        # Default attack move if no enemies in sight
        if not enemies:
            for unit in agents:
                self.actions_list.append(attack(unit, self.enemy_position, visible_matrix))
        
        return self.actions_list