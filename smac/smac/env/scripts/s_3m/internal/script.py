from s2clientprotocol import common_pb2 as sc_common
from s2clientprotocol import sc2api_pb2 as sc_pb
from s2clientprotocol import raw_pb2 as r_pb
from s2clientprotocol import debug_pb2 as d_pb


actions = {
    "move": 16,  # target: PointOrUnit
    "attack": 23,  # target: PointOrUnit
    "stop": 4,  # target: None
    "heal": 386,  # Unit
}

def script(obs, iteration):

    actions_list = []

    for unit in obs.observation.raw_data.units:
        if unit.owner == 2:
            cmd = r_pb.ActionRawUnitCommand(
                    ability_id=actions["attack"],
                    target_world_space_pos=sc_common.Point2D(
                        x=9, y=16
                    ),
                    unit_tags=[unit.tag],
                    queue_command=False,
                )
            sc_action = sc_pb.Action(action_raw=r_pb.ActionRaw(unit_command=cmd))
            actions_list.append(sc_action)

    return actions_list