from numpy import ndarray

from game_object import GameObj


class Building(GameObj):
    def __init__(self, health: int, start_pos: ndarray, size: ndarray, char_repr: str, game):
        super().__init__(health, start_pos, size, char_repr, game)

    def update_colours(self):
        super().update_colours()