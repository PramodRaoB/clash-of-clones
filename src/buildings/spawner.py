import time

from numpy import ndarray

from src.buildings.building import Building
from src import config as conf
from src.characters.barbarian import Barbarian
from src.utils import wait


class Spawner(Building):
    KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    def __init__(self, start_pos: ndarray, char_repr: str, game):
        super().__init__(1, start_pos, conf.SPAWNER_SIZE, char_repr, False, game, conf.SPAWNER_COOLDOWN)

    def attack(self):
        if wait(self.last_attack, self.cooldown):
            return False
        self.last_attack = time.time()
        return True

    def update(self):
        return self.attack()
