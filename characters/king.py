import numpy as np

import config as conf
from characters.character import Character


class King(Character):
    KEYS = ['w', 'a', 's', 'd', ' ']
    DX = [-1, 0, 1, 0]
    DY = [0, -1, 0, 1]

    def __init__(self, start_pos, game):
        super().__init__(conf.KING_HP, start_pos, 'K', game)

    def move(self, inp: str):
        ind = King.KEYS.index(inp)
        super().move(np.array([King.DX[ind], King.DY[ind]]))
