import numpy as np

from src import config as conf
from src.characters.character import Character
from src.characters.playable import Playable
from src.utils import wait, play_audio


class Queen(Playable):

    def __init__(self, start_pos, game):
        self._last_moved = 3
        super().__init__(conf.QUEEN_HP, conf.QUEEN_DAMAGE, conf.QUEEN_SPEED, start_pos, '☥', game, conf.QUEEN_COOLDOWN,
                         conf.QUEEN_RADIUS)

    def move(self, inp: str):
        ret = super().move(inp)
        if ret is not None:
            self._last_moved = ret

    def attack(self):
        coords = np.empty((0, 2), int)
        for i in range(self.start_pos[0] - self._radius, self.start_pos[0] + self._radius + 1):
            for j in range(self.start_pos[1] - self._radius, self.start_pos[1] + self._radius + 1):
                coords = np.append(coords, np.array([[i, j]]), axis=0)
        for i in range(len(coords)):
            coords[i][0] += Character.DX[self._last_moved] * conf.QUEEN_RANGE
            coords[i][1] += Character.DY[self._last_moved] * conf.QUEEN_RANGE

        if not super().attack(coords):
            return False
        else:
            play_audio("src/assets/swing.mp3")
