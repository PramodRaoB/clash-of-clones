import time

from src import config as conf


class Spell:
    KEYS = ['r', 'h']

    def __init__(self, game, factor, color, duration=0):
        self._duration = duration
        self._factor = factor
        self.game = game
        self._init_time = time.time()
        self._effect_color = color
        self.is_over = False

    def update(self):
        for c in self.game.characters:
            if c is not None and not c.is_dead():
                if time.time() - self._init_time < self._duration:
                    c.update_colours(self._effect_color)
                    self.affect(c)
                else:
                    self.is_over = True
                    c.update_colours(conf.BG_COLOUR)
                    self.revert(c)

    def affect(self, obj):
        pass

    def revert(self, obj):
        pass
