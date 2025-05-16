import math
from .utils.distance_api import *
from .utils.actions_api import *
from .utils.units_api import *

from .unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name

    def script(self, agents, enemies, iteration):

        return []


'''
cmd = r_pb.ActionRawUnitCommand(
        ability_id=actions["stop"],
        unit_tags=[tag],
        queue_command=False,
    )
'''