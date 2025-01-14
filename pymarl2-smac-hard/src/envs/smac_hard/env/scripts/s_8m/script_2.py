import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

actions = {
    "move": 16,  # target: PointOrUnit
    "attack": 23,  # target: PointOrUnit
    "stop": 4,  # target: None
    "heal": 386,  # Unit
}
class DecisionTreeScript():

    def __init__(self, map_name):

        self.map_name = map_name


    def script(self, obs, iteration):
        

        self.actions_list = []

        units = [unit for unit in obs.observation.raw_data.units if unit.owner==2]
        enemy_units = [unit for unit in obs.observation.raw_data.units if unit.owner==1]

        marines = sorted([unit for unit in units if unit.unit_type==UnitTypeId.MARINE.value], key=lambda u: u.tag)
        enemy_marines = [unit for unit in enemy_units if unit.unit_type==MAP_UNITS_TYPES[self.map_name]['enemy'][0]]
        
        # Origin Policy.
        for m in marines:
            self.actions_list.append(attack(m, (9, 16)))
        

        return self.actions_list


'''
cmd = r_pb.ActionRawUnitCommand(
        ability_id=actions["stop"],
        unit_tags=[tag],
        queue_command=False,
    )
'''