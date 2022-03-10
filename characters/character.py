from game_object import GameObj
import config as conf


class Character(GameObj):
    def __init__(self, health, start_pos, char_repr, game):
        super().__init__(health, start_pos, [1, 1], char_repr, game)

    def get_current_color(self):
        health_ratio = self.health / self.max_health
        if health_ratio > 0.8:
            return conf.CHAR_HEALTH0
        elif health_ratio > 0.6:
            return conf.CHAR_HEALTH1
        elif health_ratio > 0.4:
            return conf.CHAR_HEALTH2
        elif health_ratio > 0.2:
            return conf.CHAR_HEALTH3
        else:
            return conf.CHAR_HEALTH4
