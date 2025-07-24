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
        self.init = True
        self.map_name = map_name
        self.engage = True

    def script(self, obs, iteration):
        

        self.actions_list = []

        units = [unit for unit in obs.observation.raw_data.units if unit.owner==2]
        enemy_units = [unit for unit in obs.observation.raw_data.units if unit.owner==1]

        marines = sorted([unit for unit in units if unit.unit_type==UnitTypeId.MARINE.value], key=lambda u: u.tag)
        enemy_marines = [unit for unit in enemy_units if unit.unit_type==MAP_UNITS_TYPES[self.map_name]['enemy'][0]]
        
        if self.init:
            self.pre_health = {}
            self.cur_health = {}
            for m in marines:
                self.pre_health[m.tag] = 1
                self.cur_health[m.tag] = 1
            self.init = False

        if not marines or not enemy_marines:
            return []
        
        for m in marines:
            self.cur_health[m.tag] = m.health/m.health_max

        # Form marines according to a line on (25, 16) through 5 iterations
        if iteration < 5:
            for i, m in enumerate(marines):
                # m.move(self.start_location + (-3, (i-len(marines)/2)*1))
                self.actions_list.append(move(m, (25, 16+(i-len(marines)/2))))
        elif min([distance_to(e, center(marines)) for e in enemy_marines]) > 8 and self.engage:
            for m in marines:
                self.actions_list.append(move(m, (m.pos.x-1, m.pos.y)))
        else:
            self.engage = False
            target = min(enemy_marines, key=lambda e: math.fabs(e.pos.x-center(marines)[0]))
            for i, m in enumerate(marines):

                if self.pre_health[m.tag] != self.cur_health[m.tag] and m.health/m.health_max < 0.3:
                    self.actions_list.append(move(m, (m.pos.x+1, m.pos.y)))
                else:
                    # marine.attack(target)
                    self.actions_list.append(attack(m, target))
            
        for m in marines:
            self.pre_health[m.tag] = self.cur_health[m.tag]

        return self.actions_list


'''
cmd = r_pb.ActionRawUnitCommand(
        ability_id=actions["stop"],
        unit_tags=[tag],
        queue_command=False,
    )
'''