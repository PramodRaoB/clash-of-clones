import config as conf
from characters.character import Character


class King(Character):
    KEYS = ['w', 'a', 's', 'd', ' ']

    def __init__(self, start_pos, game):
        super().__init__(conf.KING_HP, start_pos, 'K', game)
