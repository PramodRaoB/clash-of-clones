from buildings.building import Building
import config as conf


class TownHall(Building):
    def __init__(self, start_pos, game):
        super().__init__(conf.TOWNHALL_HP, start_pos, conf.TOWNHALL_SIZE, 'T', game)
