import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId
from ..rl_unit_typeid import RLUnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name
        

    def script(self, obs, iteration):
        
        self.actions_list = []
        units = [unit for unit in obs.observation.raw_data.units if unit.owner==2]
        enemy_units = [unit for unit in obs.observation.raw_data.units if unit.owner==1]

        zealots = sorted([unit for unit in units if unit.unit_type==UnitTypeId.ZEALOT.value], key=lambda u: u.tag)
        enemy_stalkers = sorted([unit for unit in enemy_units if unit.unit_type==MAP_UNITS_TYPES[self.map_name]['enemy'][0]], key=lambda u:u.tag)
        


        if not zealots or not enemy_stalkers:
            return []
        
        groups = [[] for _ in range(len(enemy_stalkers))]

        # Allocate zealots to groups
        for i, z in enumerate(zealots):
            groups[i % len(enemy_stalkers)].append(z)

        for i, g in enumerate(groups):

            for z in g:
                self.actions_list.append(attack(z, enemy_stalkers[i]))


        return self.actions_list

    
        