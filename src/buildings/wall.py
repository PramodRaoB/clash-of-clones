from numpy import ndarray

from src.buildings.building import Building
from src import config as conf


class Wall(Building):
    def __init__(self, start_pos: ndarray, game):
        super().__init__(conf.WALL_HP, start_pos, conf.WALL_SIZE, 'W', game)
