import time

from numpy import ndarray

from src.buildings.building import Building
from src import config as conf
from src.characters.barbarian import Barbarian
from src.utils import wait


class Spawner(Building):
    KEYS = ['1', '2', '3']

    def __init__(self, start_pos: ndarray, game):
        super().__init__(1, start_pos, conf.SPAWNER_SIZE, 'x', game, conf.SPAWNER_COOLDOWN)

    def attack(self):
        if wait(self.last_attack, self.cooldown):
            return False
        self.last_attack = time.time()
        new_barb = Barbarian(self.start_pos.copy(), self.game)
        self.game.barbs.append(new_barb)
        self.game.characters.append(new_barb)
        return True

    def update(self):
        return self.attack()
