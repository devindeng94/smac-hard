import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name

    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):
        
        self.actions_list = []

        marines = [agent for _, agent in agents.items() if agent.health != 0]
        enemy_marines = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        if not marines or not enemy_marines:
            return []
        
        if iteration < 10:
            self.update_formation(marines)
            return self.actions_list
        
        # Move left
        if min([distance_to(center(marines), em) for em in enemy_marines]) > 9:
            for marine in marines:
                self.actions_list.append(move_point(marine, marine.pos.x-2, marine.pos.y))
        else:
            for marine in marines:
                target = nearest_n_units(marine, enemy_marines, 5)
                weakest_target = min(target, key=lambda e: e.health)

                self.actions_list.append(attack(marine, (weakest_target.pos.x, weakest_target.pos.y), visible_matrix))

        return self.actions_list

    def update_formation(self, marines):

        marines_sorted = sorted(marines, key=lambda m: m.pos.y)

        for i, marine in enumerate(marines_sorted):
            position = (25, 16 + (i - len(marines) / 2) * 0.65)
            self.actions_list.append(move_point(marine, position[0], position[1]))
        self.formation = marines_sorted
    
        