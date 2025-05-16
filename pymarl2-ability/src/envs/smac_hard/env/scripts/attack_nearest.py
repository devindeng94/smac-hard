import math
import pdb
from .utils.distance_api import *
from .utils.actions_api import *
from .utils.units_api import *

from .unit_typeid import UnitTypeId

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name

    def script(self, agents, enemies, agent_ability, iteration):

        actions = []
        
        # Change from dict to list
        agents = [agent for _, agent in agents.items() if agent.health != 0]
        enemies = [enemy for _, enemy in enemies.items() if enemy.health != 0]

        if not agents or not enemies:
            return []


        weakest_agent = min(agents, key=lambda e: e.health / e.health_max)

        for agent in agents:
            
            nearest_enemy = min(enemies, key=lambda e: distance_to(agent, e))
            if agent.unit_type == UnitTypeId.MEDIVAC.value:
                actions.append(move(agent,(weakest_agent.pos.x+2, weakest_agent.pos.y)))
            else:
                actions.append(attack(agent, (nearest_enemy.pos.x, nearest_enemy.pos.y)))            
        
        return actions


