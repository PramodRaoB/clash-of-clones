import sys
import time

import numpy as np
from numpy import ndarray

from src import config as conf
from src.characters.character import Character
from src.utils import wait, play_audio


class Balloon(Character):
    def __init__(self, start_pos, game):
        super().__init__(conf.BALLOON_HP, conf.BALLOON_DAMAGE, conf.BALLOON_SPEED, start_pos, '0', game,
                         conf.BALLOON_COOLDOWN)

    def move(self):
        if wait(self.last_move, self.movement_speed):
            return
        target = self.get_closest_target()
        if target is None:
            return
        target_pos = target[0][1]
        move_dir = np.array([0, 0])
        for i in range(0, 2):
            if target_pos[i] > self.start_pos[i]:
                move_dir[i] += 1
            elif target_pos[i] < self.start_pos[i]:
                move_dir[i] -= 1

        if move_dir[0] == 0 and move_dir[1] == 0:
            self.attack(target[1])
        else:
            self.last_move = time.time()
            self.start_pos += move_dir
            if self.game.scene.is_out(self.start_pos):
                self.start_pos -= move_dir

    def get_target_from_me(self):
        ret = []
        for building in self.game.buildings:
            if building is not None and not building.is_dead() and building.is_defensive:
                ret.append((self.distance_to(building), building))

        if len(ret) == 0:
            ret = super().get_target_from_me()

        return ret

    def attack(self, target_obj):
        if wait(self.last_attack, self.cooldown):
            return
        self.last_attack = time.time()
        play_audio("src/assets/balloon_attack.mp3")
        target_obj.take_damage(self.damage)

    def update(self):
        self.move()
