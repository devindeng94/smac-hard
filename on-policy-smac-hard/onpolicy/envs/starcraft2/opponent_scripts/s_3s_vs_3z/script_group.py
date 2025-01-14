import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name
        self.init = True
        self.target_dict = {}

    def script(self, obs, iteration):
        
        self.actions_list = []
        units = [unit for unit in obs.observation.raw_data.units if unit.owner==2]
        enemy_units = [unit for unit in obs.observation.raw_data.units if unit.owner==1]

        zealots = sorted([unit for unit in units if unit.unit_type==UnitTypeId.ZEALOT.value], key=lambda u: u.tag)
        enemy_stalkers = [unit for unit in enemy_units if unit.unit_type==MAP_UNITS_TYPES[self.map_name]['enemy'][0]]
        
        if self.init:
            for i, zealot in enumerate(zealots):
                self.target_dict[zealot.tag] = enemy_stalkers[i%len(enemy_stalkers)]
            self.init = False


        if not zealots or not enemy_stalkers:
            return []
        
        
        # Allocate zealots to groups
        for i, z in enumerate(zealots):
            target = self.target_dict[z.tag]
            if not target.is_active:
                target = nearest_n_units(z, enemy_stalkers, 1)[0]
                self.target_dict[z.tag] = target

            self.actions_list.append(attack(z, target))

        return self.actions_list

    
        