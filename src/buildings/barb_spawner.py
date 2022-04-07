from numpy import ndarray

from src.buildings.spawner import Spawner
from src.characters.barbarian import Barbarian


class BarbSpawner(Spawner):
    KEYS = ['1', '2', '3']

    def __init__(self, start_pos: ndarray, game):
        super().__init__(start_pos, 'x', game)

    def attack(self):
        if not super().attack():
            return False
        new_barb = Barbarian(self.start_pos.copy(), self.game)
        self.game.barbs.append(new_barb)
        self.game.characters.append(new_barb)
        return True

    def update(self):
        return self.attack()
