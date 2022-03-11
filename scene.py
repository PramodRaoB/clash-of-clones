import sys

from numpy import ndarray

import config as conf
import numpy as np

from game_object import GameObj


class Scene:
    DEFAULT = conf.BG_COLOUR + ' '

    def __init__(self, size: ndarray):
        self.frame = None
        self._size = size
        self.clear()

    def move_cursor(self, y, x):
        print("\033[%d;%dH" % (y, x))

    def clear(self):
        self.frame = np.array([[Scene.DEFAULT for j in range(self._size[1])] for i in range(self._size[0])],
                              dtype='object')

    def display(self):
        self.move_cursor(0, 0)
        print_screen = ''
        for i in range(self._size[0]):
            for j in range(self._size[1]):
                print_screen += self.frame[i][j]
            print_screen += '\n'
        sys.stdout.write(print_screen)

    def add_object(self, obj: GameObj):
        self.frame[obj.start_pos[0]:obj.start_pos[0] + obj.size[0],
        obj.start_pos[1]:obj.start_pos[1] + obj.size[1]] = obj.repr
