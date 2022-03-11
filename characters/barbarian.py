import numpy as np

import config as conf
from characters.character import Character


class Barbarian(Character):
    def __init__(self, start_pos, game):
        super().__init__(conf.BARB_HP, conf.BARB_DAMAGE, conf.BARB_SPEED, start_pos, '!', game)

    def move(self):
        target = self.get_closest_building()
        if target is None:
            return
        target_pos = target[0][1]
        move_dir = np.array([0, 0])
        for i in range(0, 2):
            if target_pos[i] > self.start_pos[i]:
                move_dir[i] += 1
            elif target_pos[i] < self.start_pos[i]:
                move_dir[i] -= 1

        ret_structure = self.game.get_structure_on_coord(self.start_pos + move_dir)
        if ret_structure is not None:
            self.attack(ret_structure)
        else:
            super().move(move_dir)

    def attack(self, target_obj):
        target_obj.take_damage(self._damage)
