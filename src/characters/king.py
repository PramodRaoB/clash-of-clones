import numpy as np

from src import config as conf
from src.characters.playable import Playable
from src.utils import wait, play_audio


class King(Playable):

    def __init__(self, start_pos, game):
        super().__init__(conf.KING_HP, conf.KING_DAMAGE, conf.KING_SPEED, start_pos, 'P', game, conf.KING_COOLDOWN,
                         conf.KING_RADIUS)

    def attack(self):
        coords = np.empty((0, 2), int)
        for i in range(self.start_pos[0] - self._radius, self.start_pos[0] + self._radius + 1):
            for j in range(self.start_pos[1] - self._radius, self.start_pos[1] + self._radius + 1):
                if abs(i - self.start_pos[0]) + abs(j - self.start_pos[1]) <= self._radius:
                    coords = np.append(coords, np.array([[i, j]]), axis=0)
        if not super().attack(coords):
            return False
        else:
            play_audio("src/assets/swing.mp3")
