import time

import numpy as np
from numpy import ndarray

from src import config as conf
from src.characters.character import Character
from src.utils import wait, play_audio


class Playable(Character):
    KEYS = ['w', 'a', 's', 'd', ' ']

    def __init__(self, health: int, damage: int, speed, start_pos: ndarray, char_repr: str, game, cooldown, radius):
        self._radius = radius
        super().__init__(health, damage, speed, start_pos, char_repr, game, cooldown)

    def move(self, inp: str):
        if wait(self.last_move, self.movement_speed):
            return None
        self.last_move = time.time()
        ind = Playable.KEYS.index(inp)
        super().move(np.array([Character.DX[ind], Character.DY[ind]]))
        return ind

    def attack(self, coords):
        if wait(self.last_attack, self.cooldown):
            return False
        self.last_attack = time.time()
        super().attack(coords)
        return True
