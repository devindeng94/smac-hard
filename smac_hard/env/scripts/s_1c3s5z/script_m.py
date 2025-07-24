import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name


    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):

        self.actions_list = []

        self.units = [agent for _, agent in agents.items() if agent.health != 0]
        self.enemy_units = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        
        stalkers = [unit for unit in self.units if unit.unit_type==UnitTypeId.STALKER.value]
        zealots = [unit for unit in self.units if unit.unit_type==UnitTypeId.ZEALOT.value]
        colossi = [unit for unit in self.units if unit.unit_type==UnitTypeId.COLOSSUS.value]

        if not stalkers and not zealots and not colossi:
            return []
        
        if not self.enemy_units:
            return []
        
        army_center = center(stalkers + zealots + colossi)

        if self.units_too_spread(army_center):
            for unit in self.units:
                self.actions_list.append(move(unit, army_center))
        
        for zealot in zealots:
            closest_enemy = min(self.enemy_units, key=lambda e: distance_to(e, zealot))
            self.actions_list.append(attack(zealot, closest_enemy, visible_matrix))

        for stalker in stalkers:
            closest_enemy = min(self.enemy_units, key=lambda e: distance_to(e, stalker))
            self.actions_list.append(attack(stalker, closest_enemy, visible_matrix))

        for colossus in colossi:
            if self.enemy_units:
                best_target = self.find_best_attack_target(self.enemy_units)
                if best_target == None:
                    best_target = closest_enemy = min(self.enemy_units, key=lambda e: distance_to(e, colossus))
                self.actions_list.append(attack(colossus, best_target, visible_matrix))

        return self.actions_list

    def units_too_spread(self, army_center):

        return any(distance_to(unit, army_center) > 12 for unit in self.units)

    def find_best_attack_target(self, enemies):

        best_target = None
        highest_density = -1

        for enemy in enemies:
            nearby_enemies = closer_than(enemy, enemies, 3)
            if len(nearby_enemies) > highest_density:
                highest_density = len(nearby_enemies)
                best_target = enemy

        return best_target
        

