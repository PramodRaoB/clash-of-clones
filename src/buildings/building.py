import time

from numpy import ndarray
from src import config as conf

from src.game_object import GameObj


class Building(GameObj):
    def __init__(self, health: int, start_pos: ndarray, size: ndarray, char_repr: str, is_defensive, game, cooldown=0):
        self.is_defensive = is_defensive
        super().__init__(health, start_pos, size, char_repr, game, cooldown)

    def get_current_color(self):
        time_elapsed = time.time() - self.last_attack
        if time_elapsed < self.cooldown / 2:
            output_color = conf.CANNON1
        else:
            output_color = conf.CANNON0

        if self.health / self.max_health > 0.5:
            return output_color + conf.HEALTH0
        elif self.health / self.max_health > 0.2:
            return output_color + conf.HEALTH1
        else:
            return output_color + conf.HEALTH2

    def update_colours(self):
        super().update_colours()
