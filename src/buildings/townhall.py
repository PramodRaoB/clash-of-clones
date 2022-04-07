from numpy import ndarray

from src.buildings.building import Building
from src import config as conf


class TownHall(Building):
    def __init__(self, start_pos: ndarray, game):
        super().__init__(conf.TOWNHALL_HP, start_pos, conf.TOWNHALL_SIZE, 'T', game)
