import errno
import os
import sys
import pickle

from numpy import ndarray
from colorama import Fore, Style

import src.config as conf
import numpy as np

from src.game_object import GameObj
from src.utils import numbers, play_audio


class Scene:
    DEFAULT = conf.BG_COLOUR + ' '

    def __init__(self, size: ndarray):
        self._all_frames = np.array([])
        self.frame = None
        self._size = size
        self.clear()

    def move_cursor(self, y, x):
        return "\033[" + str(y) + ";" + str(x) + "H"

    def clear(self):
        self.frame = np.array([[Scene.DEFAULT for j in range(self._size[1])] for i in range(self._size[0])],
                              dtype='object')

    def display(self):
        print_screen = self.move_cursor(8, 0)
        for i in range(self._size[0]):
            for j in range(self._size[1]):
                print_screen += self.frame[i][j]
            print_screen += '\n'
        self._all_frames = np.append(self._all_frames, print_screen)
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

    def save_replay(self):
        ret = numbers("./replays")
        count = 1
        for cnt in ret:
            count = max(count, cnt + 1)
        file_name = "./replays/replay" + str(count)
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(file_name, 'wb') as handle:
            pickle.dump(self._all_frames, handle)

    def game_over(self, won, score, time_elapsed, barbs, archers, balloons, rage, heal):
        os.system("clear")
        print_screen = self.move_cursor(int(self._size[0] / 2), int(self._size[1] / 2))
        os.system("pkill mpg123")
        if won:
            print_screen += Fore.GREEN + Style.BRIGHT
            print_screen += "You won!\n"
            play_audio("src/assets/yes.mp3")
        else:
            print_screen += Fore.RED + Style.BRIGHT
            print_screen += "You lost!\n"
            play_audio("src/assets/no.mp3")

        print_screen += "You scored: " + str(score) + "\n"
        print_screen += "You survived for: " + str(time_elapsed) + "s\n"
        print_screen += "You expended: \n" \
                        + str(barbs) + f" barbarians,\n{archers} archers,\n{balloons} balloons,\n" + str(
                            rage) + " rages,\n" + str(heal) + " heals\n"
        print_screen += "\n\n\n"
        self._all_frames = np.append(self._all_frames, print_screen)
        self.save_replay()
        sys.stdout.write(print_screen)

    def hud(self, score, time_elapsed, barbs, archers, balloons, rage, heal, health=0, max_health=100):
        print_screen = self.move_cursor(0, 0)
        print_screen += "PLayer health: "
        for i in range(int(health * 10 / max_health)):
            print_screen += "❤"
        for i in range(int((max_health - health) * 10 / max_health) + 10):
            print_screen += " "
        print_screen += "\n"
        print_screen += "Score: " + str(score) + "\n"
        print_screen += "Time elapsed: " + str(time_elapsed) + "s\n"
        print_screen += "You expended: \n" \
                        + str(barbs) + f" barbarians, {archers} archers, {balloons} balloons, " + str(
                            rage) + " rages, " + str(heal) + " heals\n"
        sys.stdout.write(print_screen)
