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
        
        stalkers = [unit for unit in obs.observation.raw_data.units if unit.owner==1]
        enemy_spine_crawler = [unit for unit in obs.observation.raw_data.units if unit.owner==2][0]
        
        # Define initial positions and retreat positions
        initial_positions = [(11, 9), (17, 9)]
        retreat_positions = [(4, 7),(23, 7)]

        # Define attack positions
        attack_positions = [(13, 21), (15, 21)]

        # Define health threshold for retreating
        health_threshold = 200  # Increase threshold to allow more damage before retreating

        # Define final assault condition
        final_assault_health = 100  # Lower threshold for final assault

        should_final_assault = enemy_spine_crawler.health < final_assault_health
        # Assign Stalkers to positions
        if len(stalkers) == 1:
            stalker = stalkers[0]
            if should_final_assault:
                # Final assault: both Stalkers attack without retreating
                actions_list.append(attack(stalker, enemy_spine_crawler))
            else:
                # Retreat: move to retreat positions
                pos = (stalker.pos.x, stalker.pos.y)
                dis = [distance_to(pos,  retreat_positions[0]), distance_to(pos, retreat_positions[1])]
                if dis[0] < dis[1]:
                    actions_list.append(move(stalker, retreat_positions[0]))
                else:
                    actions_list.append(move(stalker, retreat_positions[1]))
            return actions_list
                
                
        switch = 0
        pos_0 = (stalkers[0].pos.x, stalkers[0].pos.y)
        pos_1 = (stalkers[1].pos.x, stalkers[1].pos.y)
        dis_0 = [distance_to(pos_0,  initial_positions[0]), distance_to(pos_1, initial_positions[0])]
        dis_1 = [distance_to(pos_0,  initial_positions[1]), distance_to(pos_1, initial_positions[1])]
        if (dis_0[0]-dis_0[1]) * (dis_1[0]-dis_1[1]) >= 0:
            if dis_0[0]-dis_1[0] > dis_0[1]-dis_1[1]:
                switch = 1
        elif dis_0[0] > dis_0[1]:
            switch = 1
        stalker_a = stalkers[0+switch]
        stalker_b = stalkers[1-switch]

        # Check if we should engage or retreat
        combined_health = stalker_a.health + stalker_a.shield + stalker_b.health + stalker_b.shield
        should_retreat = combined_health < health_threshold
        
        if should_final_assault:
            # Final assault: both Stalkers attack without retreating
            actions_list.append(attack(stalker_a, enemy_spine_crawler))
            actions_list.append(attack(stalker_b, enemy_spine_crawler))
        elif should_retreat:
            # Retreat: move to retreat positions
            actions_list.append(move(stalker_a, retreat_positions[0]))
            actions_list.append(move(stalker_b, retreat_positions[1]))
        else:
            # Engage: Stalker A attacks first, Stalker B flanks and focuses fire
            if distance_to(stalker_a, enemy_spine_crawler) > 6:
                actions_list.append(move(stalker_a, attack_positions[0]))
            else:
                actions_list.append(attack(stalker_a, enemy_spine_crawler))

            if distance_to(stalker_b, enemy_spine_crawler) > 6:
                actions_list.append(move(stalker_b, attack_positions[1]))
            else:
                actions_list.append(attack(stalker_b, enemy_spine_crawler))

        return actions_list
