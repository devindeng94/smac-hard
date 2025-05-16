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
        self.groups = {}
        self.status = {}
        self.init = True
        
        
    def script(self, agents, enemies, agent_ability, iteration):

        agents = [agent for _, agent in agents.items() if agent.health != 0]
        enemies = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        if not agents or not enemies:
            return []
        actions = []

        if self.init:
            for agent in agents:
                self.status[agent.tag] = 'Attack'
            self.init = False

        # Assign targets to agents in groups
        for a_id, agent in enumerate(agents):

            if agent.health / agent.health_max < 0.2 and agent.shield/agent.shield_max < 0.2:
                self.status[agent.tag] = 'Retreat'
            elif agent.shield/agent.shield_max >0.8:
                self.status[agent.tag] = 'Attack'

            status = self.status[agent.tag]

            target = self.groups.get(agent.tag, None)
            if target == None or target.health == 0:
                self.groups[agent.tag] = enemies[a_id % len(enemies)]
                target = enemies[a_id % len(enemies)]
            
            if status == 'Attack':
                actions.append(attack(agent, target))
            elif status == 'Retreat':
                actions.append(move(agent, toward(agent, target, -2)))

        return actions
        