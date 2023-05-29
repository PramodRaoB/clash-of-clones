import config as conf
import numpy as np

from game_object import GameObj


class Scene:
    def __init__(self, height, width):
        self._height = height
        self._width = width

        self._frame = np.array([[conf.BG_COLOUR + ' ' for j in range(self._width)] for i in range(self._height)],
                               dtype='object')

    def move_cursor(self, y, x):
        print("\033[%d;%dH" % (y, x))

    def display(self):
        self.move_cursor(0, 0)
        print_screen = ''
        for i in range(self._height):
            for j in range(self._width):
                print_screen += self._frame[i][j]
            print_screen += '\n'
        print(print_screen)

    def add_object(self, obj: GameObj):
        self._frame[obj.start_pos[0]:obj.start_pos[0] + obj.size[0], obj.start_pos[1]:obj.start_pos[1] + obj.size[1]] = obj.repr
