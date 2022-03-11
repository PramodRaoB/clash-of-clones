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
        # return "\033[%d;%dH" % (y, x))
        return "\033[" + str(y) + ";" + str(x) + "H"

    def clear(self):
        self.frame = np.array([[Scene.DEFAULT for j in range(self._size[1])] for i in range(self._size[0])],
                              dtype='object')

    def display(self):
        # self.move_cursor(0, 0)
        print_screen = self.move_cursor(0, 0)
        for i in range(self._size[0]):
            for j in range(self._size[1]):
                print_screen += self.frame[i][j]
            print_screen += '\n'
        sys.stdout.write(print_screen)

    def is_out(self, coord: ndarray):
        for i in range(0, 2):
            if coord[i] < 0:
                return True
            if coord[i] >= self._size[i]:
                return True
        return False

    def is_empty(self, coord: ndarray):
        if self.is_out(coord):
            return True

        return self.frame[coord[0]][coord[1]] == Scene.DEFAULT

    def add_object(self, obj: GameObj):
        self.frame[obj.start_pos[0]:obj.start_pos[0] + obj.size[0],
        obj.start_pos[1]:obj.start_pos[1] + obj.size[1]] = obj.repr
