from numpy import ndarray

from buildings.building import Building
import config as conf


class Wall(Building):
    def __init__(self, start_pos: ndarray, game):
        super().__init__(conf.WALL_HP, start_pos, conf.WALL_SIZE, 'W', game)
