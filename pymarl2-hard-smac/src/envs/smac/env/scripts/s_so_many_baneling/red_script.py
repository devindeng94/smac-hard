import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId
import numpy as np

class DecisionTreeScript():

    def __init__(self, map_name):
        self.map_name = map_name
        
        
    def script(self, obs, iteration):

        actions_list = []
        
        zealots = sorted([unit for unit in obs.observation.raw_data.units if unit.owner==1], key=lambda u: u.tag)
        enemy_banelings = sorted([unit for unit in obs.observation.raw_data.units if unit.owner==2], key=lambda u: u.tag)
        
        
        if not zealots or not enemy_banelings:
            return

        # Initial Setup: Position Zealots in a staggered formation to minimize splash damage
        if iteration == 0:
            for i, zealot in enumerate(zealots):
                actions_list.append(move(zealot, (zealot.pos.x + (i - len(zealots)/2) * 2, zealot.pos.y + (i - len(zealots)/2) * 2)))

        for zealot in zealots:
            closest_baneling = nearest_n_units(zealot, enemy_banelings, 1)[0]
            # Kiting Strategy: Increase retreat distance to ensure Zealots can outrun Banelings
            if distance_to(zealot, closest_baneling) < 3:
                retreat_position = (zealot.pos.x - 10, zealot.pos.y - 10)
                actions_list.append(move(zealot, retreat_position))
            # Engagement Strategy: Focus on attacking the closest Banelings first
            elif distance_to(zealot, closest_baneling) < 5:
                actions_list.append(attack(zealot, closest_baneling))
            # Shield Management: Retreat earlier at 50% shield health to allow recovery
            elif zealot.shield / zealot.shield_max < 0.5:
                retreat_position = (zealot.pos.x - 8, zealot.pos.y - 8)
                actions_list.append(move(zealot, retreat_position))

                 
        return actions_list
    

class DecisionTreeScript():


    def __init__(self):

        super().__init__()
        self.zealot_defensive = True
        self.zealot_scatter = False
        self.zealot_baiting = False
        self.scatter_points = [(5, 5), (5, 25), (25, 5), (25, 25), (15, 5), (15, 25), (5, 15)]

    def script(self, obs, iteration):
        
        zealots = sorted([unit for unit in obs.observation.raw_data.units if unit.owner==1], key=lambda u: u.tag)
        banelings = sorted([unit for unit in obs.observation.raw_data.units if unit.owner==2], key=lambda u: u.tag)

        actions_list = [None] * len(zealots)
        
        if not zealots or not banelings:
            return

        if self.zealot_defensive:
            return self.defensive_perimeter_formation(zealots, banelings, actions_list)
        elif self.zealot_scatter:
            return self.scatter_and_regroup(zealots, actions_list)
        elif len(zealots) >= 5:
            return self.bait_and_dodge(zealots, banelings, actions_list)

    def defensive_perimeter_formation(self, zealots, banelings, action_list):
        center = (15, 15)
        radius = 5
        angle_increment = 2 * 3.14159 / len(zealots)
        
        for i, zealot in enumerate(zealots):
            angle = i * angle_increment
            position = center + (radius * math.cos(angle), radius * math.sin(angle))
            action_list[i] = move(zealot, position)

        closest_baneling = nearest_n_units(center, banelings, 1)[0]
        if distance_to(closest_baneling, center) < 5:
            dis = [distance_to(z, closest_baneling) for z in zealots]
            nearest_zealot_id = np.argmin(dis)
            action_list[nearest_zealot_id] = attack(zealots[nearest_zealot_id], closest_baneling)
        return action_list

    def scatter_and_regroup(self, zealots, action_list):
        if not self.zealot_scatter:
            self.scatter_start_time = self.state.game_loop
            self.zealot_scatter = True

        for i, zealot in enumerate(zealots):
            if i < len(self.scatter_points):
                action_list.append(move(zealot, self.scatter_start_time[i]))

        if self.state.game_loop - self.scatter_start_time > 3 * 22.4:  # 3 seconds
            for zealot in zealots:
                action_list.append(move(zealot, (15, 15)))
            self.zealot_scatter = False
        return action_list

    def bait_and_dodge(self, zealots, banelings):
        action_list = []
        
        zealots_health = [z.health for z in zealots]
        
        bait_id = np.argmin(zealots_health)
        self.bait_zealot = zealots[bait_id]

        banelings_center = center(banelings)
        
        bait_position = toward(banelings_center, self.bait_zealot, 3)
        action_list.append(move(self.bait_zealot, bait_position))

        arc_zealots = [zealots[i] for i in range(len(zealots)) if i != bait_id]
        arc_positions = [toward(bait_position, self.bait_zealot, 5) for _ in range(len(arc_zealots))]

        for i, zealot in enumerate(arc_zealots):
            if i < len(arc_positions):
                action_list.append(move(zealot, arc_positions[i]))

        if distance_to(nearest_n_units(self.bait_zealot, banelings, 1)[0], self.bait_zealot) < 3:
            action_list.append(move(self.bait_zealot, (15, 15)))
            for zealot in arc_zealots:
                closest_baneling = nearest_n_units(zealot, banelings, 1)[0]
                action_list.append(attack(zealot, closest_baneling))

