from s2clientprotocol import common_pb2 as sc_common
from s2clientprotocol import sc2api_pb2 as sc_pb
from s2clientprotocol import raw_pb2 as r_pb
from s2clientprotocol import debug_pb2 as d_pb

from ...unit_typeid import UnitTypeId
from ...rl_unit_typeid import RLUnitTypeId

actions = {
    "move": 16,  # target: PointOrUnit
    "attack": 23,  # target: PointOrUnit
    "stop": 4,  # target: None
    "heal": 386,  # Unit
}

def script(obs, iteration):

    units = [unit for unit in obs.observation.raw_data.units if unit.owner==2]
    enemy_units = [unit for unit in obs.observation.raw_data.units if unit.owner==1]


    actions_list = []

    marines = [unit for unit in units if unit.unit_type==UnitTypeId.MARINE.value]
    enemy_marines = [unit for unit in enemy_units if unit.unit_type==RLUnitTypeId.RL_MARINE.value]
    

    if not marines or not enemy_marines:
        return []
    
    target = min(enemy_marines, key=lambda e: e.health)
    for marine in marines:

        # marine.attack(target)
        cmd = r_pb.ActionRawUnitCommand(
                ability_id=actions["attack"],
                target_unit_tag=target.tag,
                unit_tags=[marine.tag],
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