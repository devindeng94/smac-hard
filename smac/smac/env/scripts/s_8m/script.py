from s2clientprotocol import common_pb2 as sc_common
from s2clientprotocol import sc2api_pb2 as sc_pb
from s2clientprotocol import raw_pb2 as r_pb
from s2clientprotocol import debug_pb2 as d_pb

from ..unit_typeid import UnitTypeId
from ..rl_unit_typeid import RLUnitTypeId

actions = {
    "move": 16,  # target: PointOrUnit
    "attack": 23,  # target: PointOrUnit
    "stop": 4,  # target: None
    "heal": 386,  # Unit
}
class DecisionTreeScript():

    def __init__(self):
        self.pre_health = [1 for _ in range(8)]
        self.cur_health = [1 for _ in range(8)]

    def script(self, obs, iteration):
        
        units = [unit for unit in obs.observation.raw_data.units if unit.owner==2]
        enemy_units = [unit for unit in obs.observation.raw_data.units if unit.owner==1]

        marines = sorted([unit for unit in units if unit.unit_type==UnitTypeId.MARINE.value], key=lambda u: u.tag)
        enemy_marines = [unit for unit in enemy_units if unit.unit_type==RLUnitTypeId.RL_MARINE.value]
        

        if not marines or not enemy_marines:
            return []
        
        self.cur_health = [m.health/m.health_max for m in marines]
        attacked = [ph != ch for ph, ch in zip(self.pre_health, self.cur_health)]

        actions_list = []
        # Form marines according to a line on (25, 16) through 5 iterations
        if iteration < 5:
            for i, m in enumerate(marines):
                # m.move(self.start_location + (-3, (i-len(marines)/2)*1))
                cmd = r_pb.ActionRawUnitCommand(
                    ability_id=actions["move"],
                    target_world_space_pos=sc_common.Point2D(
                        x=25, y=16+(i-len(marines)/2)
                    ),
                    unit_tags=[m.tag],
                    queue_command=False,
                ) 
                sc_action = sc_pb.Action(action_raw=r_pb.ActionRaw(unit_command=cmd))
                actions_list.append(sc_action) 

        else:
            target = min(enemy_marines, key=lambda e: e.health)
            for i, m in enumerate(marines):

                if attacked[i] and m.health/m.health_max < 0.3:
                    cmd = r_pb.ActionRawUnitCommand(
                            ability_id=actions["move"],
                            target_world_space_pos=sc_common.Point2D(
                                x=m.pos.x+1, y=m.pos.y
                            ),
                            unit_tags=[m.tag],
                            queue_command=False,
                        ) 
                else:
                    # marine.attack(target)
                    cmd = r_pb.ActionRawUnitCommand(
                            ability_id=actions["attack"],
                            target_unit_tag=target.tag,
                            unit_tags=[m.tag],
                            queue_command=False,
                        )
                sc_action = sc_pb.Action(action_raw=r_pb.ActionRaw(unit_command=cmd))
                actions_list.append(sc_action)

        return actions_list


'''
cmd = r_pb.ActionRawUnitCommand(
        ability_id=actions["stop"],
        unit_tags=[tag],
        queue_command=False,
    )
'''