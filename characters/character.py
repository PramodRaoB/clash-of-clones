from typing import List

import numpy as np
from numpy import ndarray

from game_object import GameObj
import config as conf
from scene import Scene


class Character(GameObj):
    DX = [-1, 0, 1, 0]
    DY = [0, -1, 0, 1]

    def __init__(self, health: int, damage: int, movement_speed: int, start_pos: ndarray, char_repr: str, game):
        self._damage = damage
        self.movement_speed = movement_speed
        super().__init__(health, start_pos, np.array([1, 1]), char_repr, game)

    def get_current_color(self):
        print("this is called")
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
        if self.has_collided():
            self.start_pos -= move_dir

    def attack(self, coords: ndarray):
        super().attack(self._damage, coords)

    def get_building_dist_from_me(self):
        ret = []
        for building in self.game.buildings:
            if building is not None and not building.is_dead():
                ret.append((self.distance_to(building), building))

        return ret

    def get_closest_building(self):
        arr = self.get_building_dist_from_me()
        min_dist = self.game.size[0] + self.game.size[1]
        min_ret = None
        for i in arr:
            if i[0][0] < min_dist:
                min_dist = i[0][0]
                min_ret = i

        return min_ret
