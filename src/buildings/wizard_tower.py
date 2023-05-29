import sys
import time

import numpy as np
from numpy import ndarray

from src.buildings.building import Building
from src import config as conf
from src.utils import wait, play_audio


class WizardTower(Building):
    def __init__(self, start_pos: ndarray, game):
        self._radius = conf.WIZARD_RADIUS
        self._range = conf.WIZARD_RANGE
        self._damage = conf.WIZARD_DAMAGE
        self._colour_change = 0
        super().__init__(conf.WIZARD_HP, start_pos, conf.WIZARD_SIZE, '❄', True, game, conf.WIZARD_COOLDOWN)

    def get_target_from_me(self):
        ret = []
        for c in self.game.characters:
            if c is not None and not c.is_dead():
                ret.append((self.distance_to(c), c))

        return ret


    def attack(self):
        self.update_colours()
        if wait(self.last_attack, self.cooldown):
            return
        target = self.get_closest_target()
        if target is None:
            return
        target_dist = target[0][0]
        if target_dist > self._range:
            return
        target_pos = target[0][1]
        all_targets = set()
        for i in range(target_pos[0] - self._radius, target_pos[0] + self._radius + 1):
            for j in range(target_pos[1] - self._radius, target_pos[1] + self._radius + 1):
                all_targets.update(self.game.get_character_on_coord(np.array([i, j])))

        for i in all_targets:
            play_audio("src/assets/wizard_tower.mp3")
            i.take_damage(self._damage)
        self.last_attack = time.time()

    def update(self):
        self.attack()
