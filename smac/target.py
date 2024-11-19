
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Race, Difficulty
from sc2.ids.ability_id import AbilityId
from sc2.ids.effect_id import EffectId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.position import Point2
from sc2.unit import Unit
from sc2.units import Units
from math import cos, sin, pi
import math
import random

class BattleBot(BotAI):

    def __init__(self):

        super().__init__()
        self.engaged_enemies = {}  # Dictionary to track engaged Marine and its target
        self.retreat_position = Point2((16, 16))  # Position to retreat to
        self.health_threshold = 25  # 55% of 45 health
        self.formation = None  # Current formation

    async def on_step(self, iteration: int):
        marines = self.units(UnitTypeId.MARINE)
        enemy_marines = self.enemy_units(UnitTypeId.MARINE)

        if not marines or not enemy_marines:
            return

        # Update formation every 30 frames if it's not set yet
        if not self.formation:
            self.update_formation(marines)

        for marine in marines:
            if marine.tag not in self.engaged_enemies:
                # Find the closest enemy Marine
                closest_enemy = min(enemy_marines, key=lambda e: marine.distance_to(e))
                self.engaged_enemies[marine.tag] = closest_enemy.tag

            target_marine = self.units.find_by_tag(self.engaged_enemies[marine.tag])
            if not target_marine:
                self.engaged_enemies.pop(marine.tag, None)
                continue

            if target_marine.health < self.health_threshold:
                # Retreat to a safe distance
                retreat_distance = target_marine.distance_to(self.retreat_position) * 2
                new_position = Point2((target_marine.position.x + retreat_distance * cos(target_marine.direction),
                                       target_marine.position.y + retreat_distance * sin(target_marine.direction)))
                marine.move(new_position)
            else:
                # Engage and attack
                marine.attack(target_marine)

            # Adjust formation based on the current position
            self.adjust_formation(marine, iteration)

    def update_formation(self, marines):
        # Sort marines by their current position along the y-axis
        marines_sorted = sorted(marines, key=lambda m: m.position.y)

        # Position marines in a more dynamic line along the y-axis
        for i, marine in enumerate(marines_sorted):
            marine.move(Point2((0, 16 + (i - len(marines) / 2) * 0.75)))
        self.formation = marines_sorted

    def adjust_formation(self, marine, iteration):
        if not self.formation:
            return

        # Calculate the ideal position for the marine based on its tag
        ideal_index = self.formation.index(marine)
        ideal_position = Point2((0, 16 + (ideal_index - len(self.formation) / 2) * 0.75))

        # Move the marine towards its ideal position
        if marine.position != ideal_position:
            marine.move(ideal_position)

if __name__ == '__main__':
    bot = BattleBot()
    result = run_game(maps.get('27m_vs_30m'), [Bot(Race.Random, bot), Computer(Race.Random, Difficulty.VeryHard)], realtime=False)
    print(result)
    print(bot.state.score.score)
    print(bot.state.score.total_damage_dealt_life)
    print(bot.state.score.total_damage_taken_life)
    print(bot.state.score.total_damage_taken_shields)
    print(len(bot.units))
    print(len(bot.enemy_units)+ len(bot.enemy_structures))
