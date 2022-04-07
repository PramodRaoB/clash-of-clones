from numpy import ndarray

from src.buildings.spawner import Spawner
from src.characters.archer import Archer


class ArcherSpawner(Spawner):
    KEYS = ['4', '5', '6']

    def __init__(self, start_pos: ndarray, game):
        super().__init__(start_pos, 'y', game)

    def attack(self):
        if not super().attack():
            return False
        new_archer = Archer(self.start_pos.copy(), self.game)
        self.game.barbs.append(new_archer)
        self.game.characters.append(new_archer)
        return True

    def update(self):
        return self.attack()
