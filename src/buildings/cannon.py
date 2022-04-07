import time

from numpy import ndarray

from src.buildings.building import Building
from src import config as conf
from src.utils import wait, play_audio


class Cannon(Building):
    def __init__(self, start_pos: ndarray, game):
        self._radius = conf.CANNON_RADIUS
        self._damage = conf.CANNON_DAMAGE
        self._colour_change = 0
        super().__init__(conf.CANNON_HP, start_pos, conf.CANNON_SIZE, '{', True, game, conf.CANNON_COOLDOWN)

    def get_target_from_me(self):
        ret = []
        for c in self.game.characters:
            if c is not None and not c.is_dead():
                ret.append((self.distance_to(c), c))

        return ret


    def attack(self):
        self.update_colours()
        if wait(self.last_attack, self.cooldown):
            return
        target = self.get_closest_target()
        if target is not None:
            target_dist = target[0][0]
            if target_dist <= self._radius:
                target[1].take_damage(self._damage)
                play_audio("src/assets/cannon.mp3")
                self.last_attack = time.time()

    def update(self):
        self.attack()
