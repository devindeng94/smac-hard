import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId
import numpy as np


class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name
        self.init_assign = True
        self.target_tag_dict = {}
        self.init_positions = [(24, 15), (21, 26), (21, 4)]

    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):
        actions = []
        agents = [agent for _, agent in agents.items() if agent.health != 0]
        enemies = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        if not agents or not enemies:
            return []
        
        if self.init_assign:
            for idx, agent in enumerate(agents):
                self.target_tag_dict[agent.tag] = enemies[idx % len(enemies)].tag
            self.init_assign = False

        if iteration < 25:
            for idx, agent in enumerate(agents):
                actions.append(move(agent, self.init_positions[idx%3]))

            return actions

        for idx, agent in enumerate(agents):
            target = find_by_tag(enemies, self.target_tag_dict.get(agent.tag, None))
            if target == None or target.health == 0:
                # Reassign Target
                target = enemies[idx % len(enemies)]
                self.target_tag_dict[agent.tag] = target.tag

            actions.append(attack(agent, target, visible_matrix))
        

        return actions