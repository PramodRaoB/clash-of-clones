import time

from numpy import ndarray

from buildings.building import Building
import config as conf
from utils import wait


class Cannon(Building):
    def __init__(self, start_pos: ndarray, game):
        self._radius = conf.CANNON_RADIUS
        self._damage = conf.CANNON_DAMAGE
        self._colour_change = 0
        super().__init__(conf.CANNON_HP, start_pos, conf.CANNON_SIZE, '{', game, conf.CANNON_COOLDOWN)

    def get_target_from_me(self):
        ret = []
        for c in self.game.characters:
            if c is not None and not c.is_dead():
                ret.append((self.distance_to(c), c))

        return ret

    def get_current_color(self):
        time_elapsed = time.time() - self.last_attack
        if time_elapsed < self.cooldown / 2:
            output_color = conf.CANNON1
        else:
            output_color = conf.CANNON0

        if self.health / self.max_health > 0.5:
            return output_color + conf.HEALTH0
        elif self.health / self.max_health > 0.2:
            return output_color + conf.HEALTH1
        else:
            return output_color + conf.HEALTH2

    def attack(self):
        self.update_colours()
        if wait(self.last_attack, self.cooldown):
            return
        target = self.get_closest_target()
        if target is not None:
            target_dist = target[0][0]
            if target_dist <= self._radius:
                target[1].take_damage(self._damage)
                self.last_attack = time.time()

    def update(self):
        self.attack()
