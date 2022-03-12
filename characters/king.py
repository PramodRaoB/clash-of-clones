import time

import numpy as np

import config as conf
from characters.character import Character
from utils import wait


class King(Character):
    KEYS = ['w', 'a', 's', 'd', ' ']

    def __init__(self, start_pos, game):
        self._radius = conf.KING_RADIUS
        super().__init__(conf.KING_HP, conf.KING_DAMAGE, conf.KING_SPEED, start_pos, 'P', game)

    def move(self, inp: str):
        if wait(self.last_move, self.movement_speed):
            return
        self.last_move = time.time()
        ind = King.KEYS.index(inp)
        super().move(np.array([Character.DX[ind], Character.DY[ind]]))

    def attack(self):
        if wait(self.last_attack, self.cooldown):
            return
        self.last_attack = time.time()
        coords = np.empty((0, 2), int)
        for i in range(-self.start_pos[0], self.start_pos[0] + self._radius + 1):
            for j in range(-self.start_pos[1], self.start_pos[1] + self._radius + 1):
                if abs(i - self.start_pos[0]) + abs(j - self.start_pos[1]) <= self._radius:
                    coords = np.append(coords, np.array([[i, j]]), axis=0)
        super().attack(coords)
