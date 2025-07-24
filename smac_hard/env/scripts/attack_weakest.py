import math
import pdb
from .utils.distance_api import *
from .utils.actions_api import *
from .utils.units_api import *

from .unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name
        self.target_dict = {}   # Agent tag to Enemy tag

    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):

        actions = []
        
        # Change from dict to list
        agents = [agent for _, agent in agents.items() if agent.health != 0]
        enemies = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        if not agents or not enemies:
            return []

        if iteration < 10:
            return []

        weakest_enemy = min(enemies, key=lambda e: (e.health + e.shield) / (e.health_max + e.shield_max))
        weakest_agent = min(agents, key=lambda e: e.health / e.health_max)

        for agent in agents:
            if agent.unit_type == UnitTypeId.MEDIVAC.value:
                actions.append(move(agent,(weakest_agent.pos.x, weakest_agent.pos.y)))
            else:

                target_tag = self.target_dict.get(agent.tag, None)
                target = find_by_tag(enemies, target_tag)
                if target == None or target.health == 0:
                    
                    self.target_dict[agent.tag] = weakest_enemy.tag
                    target = weakest_enemy
                    
                actions.append(attack(agent, target, visible_matrix))                 
        
        return actions


