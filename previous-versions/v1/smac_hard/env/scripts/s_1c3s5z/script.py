import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        self.map_name = map_name
        
        self.colossus = []
        self.stalkers = []
        self.zealots = []
        self.ally_list = ['colossus', 'stalkers', 'zealots']
        
        self.enemy_colossus = []
        self.enemy_stalkers = []
        self.enemy_zealots = []
        self.enemy_list = ['enemy_colossus', 'enemy_stalkers', 'enemy_zealots']
        
    def script(self, obs, iteration):

        agents = [unit for unit in obs.observation.raw_data.units if unit.owner==2]
        enemies = [unit for unit in obs.observation.raw_data.units if unit.owner==1]

        actions_list = []
        init_unit(obs, self)

        
        total_enemies = self.enemy_colossus + self.enemy_stalkers + self.enemy_zealots
        
        rest_units = []

        # Tactic 1: Colossus Frontline Engagement
        if self.colossus:
            colossus = self.colossus[0]
            if self.enemy_colossus and distance_to(colossus, self.enemy_colossus[0]) <= 7:
                actions_list.append(attack(colossus, self.enemy_colossus[0]))
            else:
                attack_zealot = False
                for enemy_zealot in self.enemy_zealots:
                    if distance_to(colossus, enemy_zealot) <= 7:
                        actions_list.append(attack(colossus, enemy_zealot))
                        attack_zealot = True
                        break
                if not attack_zealot:
                    if self.enemy_colossus:
                        actions_list.append(move(colossus, toward(colossus, self.enemy_colossus[0], 2)))# Move slightly to avoid being surrounded
                    else:
                        rest_units.append(colossus)

        # Tactic 2: Stalker Hit-and-Run
        if self.enemy_stalkers:
            for stalker in self.stalkers:
                closest_stalker = nearest_n_units(stalker, self.enemy_stalkers, 1)[0]
                if distance_to(stalker, closest_stalker) < 6:
                    actions_list.append(attack(stalker, closest_stalker))
                else:
                    actions_list.append(move(stalker, toward(stalker, closest_stalker, -2))) # Retreat slightly
        else:
            rest_units += self.stalkers

        # Tactic 3: Zealot Flanking Maneuver
        if self.enemy_zealots:
            for zealot in self.zealots:
                closest_zealot = nearest_n_units(zealot, self.enemy_zealots, 1)[0]
                if distance_to(zealot, closest_zealot) < 0.1:
                    actions_list.append(attack(zealot, closest_zealot))
                else:
                    actions_list.append(move(zealot, toward(zealot, closest_zealot, -1))) # Retreat slightly
        else:
            rest_units += self.zealots  # Reposition to avoid being surrounded

        # Additional logic to ensure units are not idle
        for unit in rest_units:
            if total_enemies:
                actions_list.append(attack(unit, nearest_n_units(unit, total_enemies, 1)[0]))
        
        return actions_list