import math
from .utils.distance_api import *
from .utils.actions_api import *
from .utils.units_api import *

from .unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name

    def script(self, obs, iteration):

        units = [unit for unit in obs.observation.raw_data.units if unit.owner==2]
        enemy_units = [unit for unit in obs.observation.raw_data.units if unit.owner==1]

        actions = []
        if self.map_name in ['3m',
                        '8m',
                        '25m',
                        '5m_vs_6m',     
                        '8m_vs_9m',
                        '10m_vs_11m',
                        '27m_vs_30m',
                        'MMM',
                        'MMM2',
                        '2s3z',
                        '3s5z',
                        '3s5z_vs_3s6z',
                        '1c3s5z',
                        '3s_vs_3z',
                        '3s_vs_4z',
                        '3s_vs_5z',
                        ]:
            # Destination Point
            for u in units:
                actions.append(attack(u, (9, 16)))

        elif self.map_name in ['bane_vs_bane',                          
                        ]:
            for u in units:
                actions.append(attack(u, (16, 8)))
        elif self.map_name in ['so_many_baneling']:
            for u in units:
                actions.append(attack(u, (4.5, 4.5)))
        elif self.map_name in ['corridor']:
            for u in units:
                actions.append(attack(u, (4.0, 4.0)))
        elif self.map_name in ['6h_vs_8z']:
            for u in units:
                actions.append(attack(u, (14.5, 9.5)))

        return actions


'''
cmd = r_pb.ActionRawUnitCommand(
        ability_id=actions["stop"],
        unit_tags=[tag],
        queue_command=False,
    )
'''