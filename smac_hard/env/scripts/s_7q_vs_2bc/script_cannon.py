import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId
from scipy.spatial.distance import pdist, squareform
import numpy as np
import pdb

# Ability 401
class DecisionTreeScript():

    def __init__(self, map_name):
        self.map_name = map_name
        
        
    def script(self, agents, enemies, agent_ability, iteration):

        agents = [agent for _, agent in agents.items() if agent.health != 0]
        enemies = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        if not agents or not enemies:
            return []
        actions = []

        
        weakest_enemy = min(enemies, key=lambda e: e.health)
        for agent in agents:
            applied = False
            for abil in agent_ability:        
                if abil.unit_tag == agent.tag:
                    for a in abil.abilities:
                        if a.ability_id == 401:     # Cannon
                            strongest_enemy = max(enemies, key=lambda e: e.health)
                            actions.append(apply_ability(agent, 401, strongest_enemy))
                            applied = True
                            
                            break
            
            if not applied:
                actions.append(attack(agent, weakest_enemy))

        return actions
        