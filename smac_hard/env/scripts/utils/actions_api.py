from s2clientprotocol import common_pb2 as sc_common
from s2clientprotocol import sc2api_pb2 as sc_pb
from s2clientprotocol import raw_pb2 as r_pb
from s2clientprotocol import debug_pb2 as d_pb
import pdb


actions = {
    "move": 16,  # target: PointOrUnit
    "attack": 23,  # target: PointOrUnit
    "stop": 4,  # target: None
    "heal": 386,  # Unit
}

def heal(unit, target):

    if type(target) == tuple:
        x, y = target
        cmd = r_pb.ActionRawUnitCommand(
                ability_id=actions["heal"],
                target_world_space_pos=sc_common.Point2D(
                    x=x, y=y
                ),
                unit_tags=[unit.tag],
                queue_command=False,
            )

    else:

        cmd = r_pb.ActionRawUnitCommand(
                ability_id=actions["heal"],
                target_unit_tag=target.tag,
                unit_tags=[unit.tag],
                queue_command=False,
            )
    return sc_pb.Action(action_raw=r_pb.ActionRaw(unit_command=cmd))

def attack(unit, target, visible_matrix):
    
    if unit == None or target == None:
        return None

    if type(target) == tuple:
        x, y = target
        cmd = r_pb.ActionRawUnitCommand(
                ability_id=actions["attack"],
                target_world_space_pos=sc_common.Point2D(
                    x=x, y=y
                ),
                unit_tags=[unit.tag],
                queue_command=False,
            )

    else:
        if target.tag in visible_matrix['blue']:

            #pdb.set_trace()
            cmd = r_pb.ActionRawUnitCommand(
                    ability_id=actions["attack"],
                    target_unit_tag=target.tag,
                    unit_tags=[unit.tag],
                    queue_command=False,
                )
        else:
            cmd = r_pb.ActionRawUnitCommand(
                ability_id=actions["move"],
                target_world_space_pos=sc_common.Point2D(
                    x=target.pos.x, y=target.pos.y
                ),
                unit_tags=[unit.tag],
                queue_command=False,
            )
        


    return sc_pb.Action(action_raw=r_pb.ActionRaw(unit_command=cmd))

def move(unit, target):
    if type(target) == tuple:
        x, y = target
        cmd = r_pb.ActionRawUnitCommand(
            ability_id=actions["move"],
            target_world_space_pos=sc_common.Point2D(
                x=x, y=y
            ),
            unit_tags=[unit.tag],
            queue_command=False,
        )

    else:
        cmd = r_pb.ActionRawUnitCommand(
            ability_id=actions["move"],
            target_world_space_pos=sc_common.Point2D(
                x=target.pos.x, y=target.pos.y
            ),
            unit_tags=[unit.tag],
            queue_command=False,
        )
    return sc_pb.Action(action_raw=r_pb.ActionRaw(unit_command=cmd)) 

def move_point(unit, x, y):
    cmd = r_pb.ActionRawUnitCommand(
            ability_id=actions["move"],
            target_world_space_pos=sc_common.Point2D(
                x=x, y=y
            ),
            unit_tags=[unit.tag],
            queue_command=False,
        )
    return sc_pb.Action(action_raw=r_pb.ActionRaw(unit_command=cmd)) 

def apply_ability(unit, ability, target):
    if type(target) == tuple:
        x, y = target
        cmd = r_pb.ActionRawUnitCommand(
                ability_id=ability,
                target_world_space_pos=sc_common.Point2D(
                    x=x, y=y
                ),
                unit_tags=[unit.tag],
                queue_command=False,
            )
    elif target == None:
        # Apply ability to self unit
        cmd = r_pb.ActionRawUnitCommand(
                ability_id=ability,
                target_world_space_pos=None,
                unit_tags=[unit.tag],
                queue_command=False,
            )
    else:
        
        cmd = r_pb.ActionRawUnitCommand(
                ability_id=ability,
                target_unit_tag=target.tag,
                unit_tags=[unit.tag],
                queue_command=False,
            )
    return sc_pb.Action(action_raw=r_pb.ActionRaw(unit_command=cmd))