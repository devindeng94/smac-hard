import math
import random
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        self.map_name = map_name
        
        self.marines = []
        self.marauders = []
        self.medivacs = []
        self.ally_list = ['marines', 'marauders', 'medivacs']
        
        self.enemy_marines = []
        self.enemy_marauders = []
        self.enemy_medivacs = []
        self.enemy_list = ['enemy_marauders', 'enemy_marines', 'enemy_medivacs']

        self.init = True
        self.engage = True
        
    def script(self, obs, iteration):


        agents = [unit for unit in obs.observation.raw_data.units if unit.owner==2]
        enemies = [unit for unit in obs.observation.raw_data.units if unit.owner==1]

        actions_list = []
        init_unit(obs, self)

        if self.init:
            self.pre_health = {}
            self.cur_health = {}
            for m in self.marines:
                self.pre_health[m.tag] = 1
                self.cur_health[m.tag] = 1
            self.init = False
        
        
        # Tactic 1: Init forming. Marauders ahead, Marines middle in line, and Medivac last

        center_x, center_y = center(self.marines+self.marauders)
        if iteration <= 5:
            
            actions_list.append(move(self.marauders[0], (center_x-2, center_y-1)))
            actions_list.append(move(self.marauders[1], (center_x-2, center_y+1)))
            for m_idx, marine in enumerate(self.marines):
                actions_list.append(move(marine, (center_x, marine.pos.y - len(self.marines) / 2 + m_idx)))
            for medivac in self.medivacs:
                actions_list.append(move(medivac, (center_x+1, medivac.pos.y)))
            
            return actions_list
        # Tactic engage to enemy site meanwhile keep the forming. Tight condition
        if all([len(closer_than(marauder, enemies, 8))==0 for marauder in self.marauders]) and self.engage:
            for agent in agents:
                actions_list.append(move(agent, (agent.pos.x-1, agent.pos.y)))
            return actions_list
        
        self.engage = False

        # Always attack the nearest enemy

        for m in self.marines:
        
            if self.pre_health[m.tag] > self.cur_health[m.tag] and m.health/m.health_max < 0.3:
                actions_list.append(move(m, (m.pos.x+1, m.pos.y)))
            else:
                if enemies:    
                    target = nearest_n_units(m, enemies, 1)[0]
                    if target:
                        actions_list.append(attack(m, target))


        # Define front line
        if self.marines:
            front_line = (center(self.marines)[0] -2, center(self.marines)[1])
        else:
            front_line = (center(agents)[0] -2, center(agents)[1])


        for m in self.marauders:
            if m.pos.x < front_line[0]:
                if self.enemy_marines + self.enemy_marauders:
                    target = nearest_n_units(m, self.enemy_marines + self.enemy_marauders, 1)[0]
                    if target:
                        actions_list.append(attack(m, target))
            else:
                actions_list.append(move(m, (front_line[0], m.pos.y)))
                
        for medivac in self.medivacs:

            all_units = self.marines + self.marauders
            most_injured_unit = min(all_units, key=lambda u: u.health/u.health_max)
            if most_injured_unit.health != most_injured_unit.health_max:
                actions_list.append(attack(medivac, most_injured_unit))
            else:
                actions_list.append(move(medivac, (center(agents)[0]+1, center(agents)[1])))

        for m in self.marines:
            self.pre_health[m.tag] = self.cur_health[m.tag]

        return actions_list