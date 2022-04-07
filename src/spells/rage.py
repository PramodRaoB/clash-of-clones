from src.spells.spell import Spell
from src import config as conf
from src.utils import play_audio


class Rage(Spell):
    def __init__(self, game):
        play_audio("src/assets/rage.mp3")
        super().__init__(game, conf.RAGE_FACTOR, conf.RAGE_COLOUR, conf.RAGE_DURATION)

    def affect(self, obj):
        obj.damage = self._factor * obj.base_damage
        obj.movement_speed = obj.base_movement_speed / self._factor

    def revert(self, obj):
        obj.damage = obj.base_damage
        obj.movement_speed = obj.base_movement_speed
