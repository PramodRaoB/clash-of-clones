import time

import numpy as np
from numpy import ndarray

import config as conf
from utils import wait


class GameObj:
    def __init__(self, health: int, start_pos: ndarray, size: ndarray, char_repr: str, game, cooldown: int):
        self.repr = None
        self.char_repr = char_repr
        self.health = health
        self.max_health = health
        self.start_pos = start_pos
        self.size = size  # height, width
        self.game = game
        self.last_attack = time.time()
        self.cooldown = cooldown
        self.update_colours()

    def update_colours(self):
        self.repr = np.array(
            [[self.get_current_color() + self.char_repr for j in range(self.size[1])] for i in range(self.size[0])],
            dtype='object')

    def get_current_color(self):
        if self.health / self.max_health > 0.5:
            return conf.HEALTH0
        elif self.health / self.max_health > 0.2:
            return conf.HEALTH1
        else:
            return conf.HEALTH2

    def is_intersecting(self, coords: ndarray):
        for i in range(0, 2):
            if coords[i] < self.start_pos[i] or coords[i] >= self.start_pos[i] + self.size[i]:
                return False
        return True

    def take_damage(self, damage: int):
        if self.is_dead():
            return
        self.health = max(self.health - damage, 0)
        self.update_colours()

    def attack(self, damage: int, coords: ndarray):
        damaged = set()
        for c in coords:
            ret = self.game.get_structure_on_coord(c)
            if ret is not None:
                damaged.add(ret)

        for obj in damaged:
            obj.take_damage(damage)

    def is_dead(self):
        return self.health <= 0

    def distance_to(self, obj):
        ans = self.game.size[0] + self.game.size[1]
        min_point = None
        for i in range(self.start_pos[0], self.start_pos[0] + self.size[0]):
            for j in range(self.start_pos[1], self.start_pos[1] + self.size[1]):
                for k in range(obj.start_pos[0], obj.start_pos[0] + obj.size[0]):
                    for l in range(obj.start_pos[1], obj.start_pos[1] + obj.size[1]):
                        if abs(i - k) + abs(j - l) < ans:
                            ans = abs(i - k) + abs(j - l)
                            min_point = [k, l]
        return ans, min_point

    def get_target_from_me(self):
        ret = []
        for building in self.game.buildings:
            if building is not None and not building.is_dead():
                ret.append((self.distance_to(building), building))

        return ret

    def get_closest_target(self):
        arr = self.get_target_from_me()
        min_dist = self.game.size[0] + self.game.size[1]
        min_ret = None
        for i in arr:
            if i[0][0] < min_dist:
                min_dist = i[0][0]
                min_ret = i

        return min_ret
