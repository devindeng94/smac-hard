import math
from ..utils.distance_api import *
from ..utils.actions_api import *
from ..utils.units_api import *

from ..unit_typeid import UnitTypeId
import numpy as np

# Uproot 3681
# Root 3680

class DecisionTreeScript():

    def __init__(self, map_name):
        
        self.map_name = map_name
        self.center = (14.0, 21.0)
        self.attack_range = 7
        self.walk_range = 4

    def script(self, agents, enemies, agent_ability, visible_matrix, iteration):
        actions = []
        agents = [agent for _, agent in agents.items() if agent.health != 0]
        enemies = [enemy for _, enemy in enemies.items() if enemy.health != 0]
        for agent in agents:

            a_ability = [ab.abilities for ab in agent_ability if ab.unit_tag==agent.tag][0]
            avail_ability = [a.ability_id for a in a_ability]

            if agent.unit_type == 140:
                # Uprooted Spore Crawler
                target = min(enemies, key=lambda e: distance_to(e, agent))

                if distance_to(agent, self.center) > 5:
                    actions.append(move(agent, self.center))
                else:
                    if distance_to(agent, target) >= 8 and distance_to(agent, self.center) < 4:
                        actions.append(move(agent, target))
                    else:
                        if 1731 in avail_ability:
                            actions.append(apply_ability(agent, 3680, (agent.pos.x, agent.pos.y)))

            elif agent.unit_type ==99:
                # rooted Spore Crawler
                target = min(enemies, key=lambda e: distance_to(e, agent))
                if distance_to(target, agent) >= 8 or distance_to(agent, self.center) >5:
                    if 1727 in avail_ability:
                        actions.append(apply_ability(agent, 3681, None))
                else:
                    actions.append(attack(agent, target, visible_matrix))

        return actions