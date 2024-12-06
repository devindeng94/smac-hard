import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        self.map_name = map_name
        
        
    def script(self, obs, iteration):

        actions_list = []
        
        colossuses = sorted([unit for unit in obs.observation.raw_data.units if unit.owner==1], key=lambda u: u.tag)
        enemy_zerglings = sorted([unit for unit in obs.observation.raw_data.units if unit.owner==2], key=lambda u: u.tag)
        zerglings_center = center(enemy_zerglings)
        
        x = [18, 22]
        for xx, colossus in zip(x, colossuses):
            # target_enemy = nearest_n_units(zerglings_center, enemy_zerglings, 1)[0]
            # target_enemy = nearest_n_units(colossus, enemy_zerglings, 1)[0]
            # actions_list.append(attack(colossus, target_enemy))
            actions_list.append(move(colossus, (xx, 20)))
        return actions_list
            
            
        for colossus in colossuses:
        # Tighten Retreat Condition
            if colossus.shield / colossus.shield_max < 0.5 or colossus.health / colossus.health_max < 0.5:
            # if (colossus.shield + colossus.health) / (colossus.shield_max + colossus.health_max) < 0.5:
                retreat_position = (16, 9) if zerglings_center[1] > 13 else (16, 17)
                if distance_to(colossus, retreat_position) > 2:
                    actions_list.append(move(colossus, retreat_position))
                else:
                    target_enemy = nearest_n_units(zerglings_center, enemy_zerglings, 1)[0]
                    actions_list.append(attack(colossus, target_enemy))

            # Aggressive Kiting
            else:
                dis = sorted([distance_to(colossus, zergling) for zergling in enemy_zerglings])
                if dis[5] < 5:
                    kiting_position = toward(colossus, zerglings_center, -5)
                    actions_list.append(move(colossus, kiting_position))

                # Focus on AoE Damage
                elif dis[10] < 7:
                    aoe_position = toward(colossus, zerglings_center, 3)
                    actions_list.append(move(colossus, aoe_position))

                # Optimize AoE Damage Positioning
                else:
                    target_enemy = nearest_n_units(zerglings_center, enemy_zerglings, 1)[0]
                    actions_list.append(attack(colossus, target_enemy))
        return actions_list
