from numpy import ndarray

from src.buildings.spawner import Spawner
from src.characters.balloon import Balloon


class BalloonSpawner(Spawner):
    KEYS = ['7', '8', '9']

    def __init__(self, start_pos: ndarray, game):
        super().__init__(start_pos, 'z', game)

    def attack(self):
        if not super().attack():
            return False
        new_balloon = Balloon(self.start_pos.copy(), self.game)
        self.game.barbs.append(new_balloon)
        self.game.characters.append(new_balloon)
        return True

    def update(self):
        return self.attack()
