import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId
from scipy.spatial.distance import pdist, squareform
import numpy as np

class DecisionTreeScript():

    def __init__(self, map_name):
        self.map_name = map_name
        self.up_cliff = []
        self.down_cliff = []
        self.free = None
        self.init = True
        self.cliff_y = 13
        
        
    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):

        agents = [agent for _, agent in agents.items() if agent.health != 0]
        enemies = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        if not agents or not enemies:
            return []
        actions = []

        if self.init:
            self.up_cliff = [agents[0].tag, agents[1].tag]
            self.down_cliff = [agents[2].tag, agents[3].tag]
            self.free = agents[4].tag
            self.targets = {}
            self.init=False

        if len(agents) >= 4:
            # Group 1 on the cliff and Group 2 off the cliff, the free agent always chases enemies
            for agent in agents:
                nearest_target = min(enemies, key=lambda e: distance_to(e, agent))
                if agent.tag in self.up_cliff: 
                    if nearest_target.pos.y > self.cliff_y:
                        actions.append(attack(agent, nearest_target, visible_matrix))
                    else:
                        actions.append(move(agent, (16, 16)))
                elif agent.tag in self.down_cliff:
                    if nearest_target.pos.y < self.cliff_y:
                        actions.append(attack(agent, nearest_target, visible_matrix))
                    else:
                        actions.append(move(agent, (16, 9)))
                elif agent.tag ==self.free:
                    actions.append(attack(agent, nearest_target, visible_matrix))
        else:
            for iter, agent in enumerate(agents):
                target = find_by_tag(enemies, self.targets[agent.tag])
                if target == None or target.health == 0:
                    target = min(enemies, key=lambda e: distance_to(e, agent))
                    self.targets[agent.tag] = target.tag
                actions.append(attack(agent, target, visible_matrix))
        
        return actions
        