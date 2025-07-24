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
        
    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):


        self.units = [agent for _, agent in agents.items() if agent.health != 0]
        self.enemy_units = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        self.marines = sorted([a for a in self.units if a.unit_type==UnitTypeId.MARINE.value], key=lambda a: a.tag)
        self.marauders = sorted([a for a in self.units if a.unit_type==UnitTypeId.MARAUDER.value], key=lambda a: a.tag)
        self.medivacs = sorted([a for a in self.units if a.unit_type==UnitTypeId.MEDIVAC.value], key=lambda a: a.tag)

        self.enemy_marines = sorted([a for a in self.enemy_units if a.unit_type==UnitTypeId.MARINE.value], key=lambda a: a.tag)
        self.enemy_marauders = sorted([a for a in self.enemy_units if a.unit_type==UnitTypeId.MARAUDER.value], key=lambda a: a.tag)
        self.enemy_medivacs = sorted([a for a in self.enemy_units if a.unit_type==UnitTypeId.MEDIVAC.value], key=lambda a: a.tag)

        if not self.units or not self.enemy_units:
            return []


        actions_list = []

        if self.init:
            self.pre_health = {}
            self.cur_health = {}
            for m in self.marines:
                self.pre_health[m.tag] = 1
                self.cur_health[m.tag] = 1
            self.init = False
        
        if self.enemy_marines:
            target_units = self.enemy_marines
        elif self.enemy_marauders:
            target_units = self.enemy_marauders
        else:
            target_units = self.enemy_units
        
        
        # Tactic 1: Init forming. Marauders ahead, Marines middle, and Medivac last

        if iteration <= 5:
            center_x, center_y = center(self.marines+self.marauders)
            for marauder in self.marauders:
                actions_list.append(move(marauder, (center_x-2, marauder.pos.y)))
            for marine in self.marines:
                actions_list.append(move(marine, (center_x, marine.pos.y)))
            for medivac in self.medivacs:
                actions_list.append(move(medivac, (center_x+1, medivac.pos.y)))
            
            return actions_list
        # Tactic engage to enemy site meanwhile keep the forming.
        if any([len(closer_than(marauder, self.enemy_units, 8))==0 for marauder in self.marauders]) and self.engage:
            for agent in self.units:
                actions_list.append(move(agent, (agent.pos.x-1, agent.pos.y)))
            return actions_list
        
        self.engage = False
        # Attack nearest zealot first, then marauders, finally medivac.

        if target_units:
            target = min(nearest_n_units(center(self.units) ,target_units, 3), key=lambda e: e.health+e.shield)
        else:
            target = random.choice(enemies)
        for m in self.marines:
        
            if self.pre_health[m.tag] > self.cur_health[m.tag] and m.health/m.health_max < 0.3:
                actions_list.append(move(m, (m.pos.x+1, m.pos.y)))
            else:    
                if target:
                    actions_list.append(attack(m, target, visible_matrix))


        # Define front line
        if self.marines:
            front_line = (center(self.marines)[0] -2, center(self.marines)[1])
        else:
            front_line = (center(self.units)[0] -2, center(self.units)[1])


        for m in self.marauders:
            if m.pos.x < front_line[0]:
                if target_units:
                    if target:
                        actions_list.append(attack(m, target, visible_matrix))
            else:
                actions_list.append(move(m, (front_line[0], m.pos.y)))
                
        for medivac in self.medivacs:

            all_units = self.marines + self.marauders
            most_injured_unit = min(all_units, key=lambda u: u.health/u.health_max)
            if most_injured_unit.health != most_injured_unit.health_max:
                actions_list.append(attack(medivac, most_injured_unit, visible_matrix))
            else:
                actions_list.append(move(medivac, (center(self.units)[0]+1, center(self.units)[1])))

        for m in self.marines:
            self.pre_health[m.tag] = self.cur_health[m.tag]

        return actions_list