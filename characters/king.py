import numpy as np

import config as conf
from characters.character import Character


class King(Character):
    KEYS = ['w', 'a', 's', 'd', ' ']

    def __init__(self, start_pos, game):
        self._radius = conf.KING_RADIUS
        super().__init__(conf.KING_HP, conf.KING_DAMAGE, conf.KING_SPEED, start_pos, 'P', game)

    def move(self, inp: str):
        ind = King.KEYS.index(inp)
        super().move(np.array([Character.DX[ind], Character.DY[ind]]))

    def attack(self):
        coords = np.array(
            [[self.start_pos[0] + i, self.start_pos[1] + j] for j in range(-self._radius, self._radius + 1) for i in range(-self._radius, self._radius + 1)])
        super().attack(coords)
