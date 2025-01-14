import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name

    def script(self, obs, iteration):

        self.actions_list = []


        units = [unit for unit in obs.observation.raw_data.units if unit.owner==2]
        enemy_units = [unit for unit in obs.observation.raw_data.units if unit.owner==1]

        actions_list = []

        marines = [unit for unit in units if unit.unit_type==UnitTypeId.MARINE.value]
        enemy_marines = [unit for unit in enemy_units if unit.unit_type==MAP_UNITS_TYPES[self.map_name]['enemy'][0]]
        

        if not marines or not enemy_marines:
            return []
        
        target = min(enemy_marines, key=lambda e: e.health)
        for marine in marines:

            # marine.attack(target)
            self.actions_list.append(attack(marine, target))
            

        return self.actions_list


'''
cmd = r_pb.ActionRawUnitCommand(
        ability_id=actions["stop"],
        unit_tags=[tag],
        queue_command=False,
    )
'''