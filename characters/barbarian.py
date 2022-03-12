import time

import numpy as np

import config as conf
from characters.character import Character
from utils import wait


class Barbarian(Character):
    def __init__(self, start_pos, game):
        super().__init__(conf.BARB_HP, conf.BARB_DAMAGE, conf.BARB_SPEED, start_pos, '!', game, conf.BARB_COOLDOWN)

    def move(self):
        if wait(self.last_move, self.movement_speed):
            return
        self.last_move = time.time()
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

        ret_structure = self.game.get_structure_on_coord(self.start_pos + move_dir)
        if ret_structure is not None:
            self.attack(ret_structure)
        else:
            super().move(move_dir)

    def attack(self, target_obj):
        if wait(self.last_attack, self.cooldown):
            return
        self.last_attack = time.time()
        target_obj.take_damage(self._damage)

    def update(self):
        self.move()
