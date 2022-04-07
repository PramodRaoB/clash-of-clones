from src.spells.spell import Spell
from src import config as conf
from src.utils import play_audio


class Heal(Spell):
    def __init__(self, game):
        super().__init__(game, conf.HEAL_FACTOR, conf.HEAL_COLOUR)
        play_audio("src/assets/heal.mp3")
        self.update()

    def affect(self, obj):
        obj.health = min(obj.health * self._factor, obj.max_health)

    def update(self):
        for c in self.game.characters:
            if c is not None and not c.is_dead():
                self.affect(c)
