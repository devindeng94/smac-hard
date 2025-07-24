import math
import pdb
from .utils.distance_api import *
from .utils.actions_api import *
from .utils.units_api import *

from .unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name
        self.target_dict = {}           #agent.tag to enemy.tag

    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):

        actions = []
        
        # Change from dict to list
        agents = [agent for _, agent in agents.items() if agent.health != 0]
        enemies = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        if not agents or not enemies:
            return []

        # Wait for 10 iterations
        if iteration < 10:
            return []

        weakest_agent = min(agents, key=lambda e: e.health / e.health_max)

        for agent in agents:
            
            if agent.unit_type == UnitTypeId.MEDIVAC.value:
                actions.append(move(agent,(weakest_agent.pos.x+2, weakest_agent.pos.y)))
            else:
                target_tag = self.target_dict.get(agent.tag, None)
                target = find_by_tag(enemies, target_tag)
                if target == None or target.health == 0:

                    nearest_enemy = min(enemies, key=lambda e: distance_to(agent, e))
                    self.target_dict[agent.tag] = nearest_enemy.tag
                    target_tag = nearest_enemy.tag


                actions.append(attack(agent, find_by_tag(enemies, target_tag), visible_matrix))            
        
        return actions


