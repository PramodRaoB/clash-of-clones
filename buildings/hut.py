from numpy import ndarray

from buildings.building import Building
import config as conf


class Hut(Building):
    def __init__(self, start_pos: ndarray, game):
        super().__init__(conf.HUT_HP, start_pos, conf.HUT_SIZE, 'H', game)
