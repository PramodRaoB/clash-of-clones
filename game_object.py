import numpy as np
from numpy import ndarray

import config as conf


class GameObj:
    def __init__(self, health: int, start_pos: ndarray, size: ndarray, char_repr: str, game):
        self.repr = None
        self.char_repr = char_repr
        self.health = health
        self.max_health = health
        self.start_pos = start_pos
        self.size = size  # height, width
        self.game = game
        self.update_colours()

    def update_colours(self):
        self.char_repr = self.get_current_color() + self.char_repr
        self.repr = np.array([[self.char_repr for j in range(self.size[1])] for i in range(self.size[0])])

    def get_current_color(self):
        if self.health / self.max_health > 0.5:
            return conf.HEALTH0
        elif self.health / self.max_health > 0.2:
            return conf.HEALTH1
        else:
            return conf.HEALTH2

