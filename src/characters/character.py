import time

import numpy as np
from numpy import ndarray

from src.game_object import GameObj
from src import config as conf


class Character(GameObj):
    DX = [-1, 0, 1, 0]
    DY = [0, -1, 0, 1]

    def __init__(self, health: int, damage: int, movement_speed: int, start_pos: ndarray, char_repr: str, game, cooldown=0):
        self.damage = damage
        self.base_damage = damage
        self.movement_speed = movement_speed
        self.base_movement_speed = movement_speed
        self.last_move = time.time()
        super().__init__(health, start_pos, np.array([1, 1]), char_repr, game, cooldown)

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
        ret_structure = self.game.get_structure_on_coord(self.start_pos)
        return ret_structure is not None

    def move(self, move_dir: ndarray):
        self.start_pos += move_dir
        if self.game.scene.is_out(self.start_pos) or self.has_collided():
            self.start_pos -= move_dir

    def attack(self, coords: ndarray):
        super().attack(self.damage, coords)

