from typing import List

import numpy as np
from numpy import ndarray

from game_object import GameObj
import config as conf
from scene import Scene


class Character(GameObj):
    def __init__(self, health: int, start_pos: ndarray, char_repr: str, game):
        super().__init__(health, start_pos, np.array([1, 1]), char_repr, game)

    def get_current_color(self):
        health_ratio = self.health / self.max_health
        if health_ratio > 0.8:
            return conf.CHAR_HEALTH0
        elif health_ratio > 0.6:
            return conf.CHAR_HEALTH1
        elif health_ratio > 0.4:
            return conf.CHAR_HEALTH2
        elif health_ratio > 0.2:
            return conf.CHAR_HEALTH3
        else:
            return conf.CHAR_HEALTH4

    def has_collided(self):
        """
            return 1 if self went out of bounds or has collided with any structure
        """
        collided = 0
        for i in range(0, 2):
            if self.start_pos[i] < 0:
                collided = 1
            if self.start_pos[i] + self.size[i] > self.game.size[i]:
                collided = 1

        if not collided:
            if self.game.scene.frame[self.start_pos[0]][self.start_pos[1]] != Scene.DEFAULT:
                collided = 1

        return collided

    def move(self, move_dir: ndarray):
        self.start_pos += move_dir
        if self.has_collided():
            self.start_pos -= move_dir
