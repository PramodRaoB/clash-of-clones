import os
import sys
import time

import config as conf
from colorama import Fore, Back, Style

from buildings.townhall import TownHall
from buildings.wall import Wall
from characters.king import King
from input import Get
from scene import Scene
from input import input_to


class Game:
    def __init__(self):
        # check if current terminal size is sufficient for the game
        self._townHall = None
        term_sz = os.get_terminal_size()
        if term_sz.lines < conf.GAME_HEIGHT or term_sz.columns < conf.GAME_WIDTH:
            print(f"{Fore.RED}{Back.BLACK}{Style.BRIGHT}Increase terminal window size to continue")
            sys.exit(1)

        self._height = conf.GAME_HEIGHT
        self._width = conf.GAME_WIDTH
        self._scene = Scene(self._height, self._width)
        self._input = Get()

        self._frame_rate = 1 / 60
        self._previous_frame = time.time()
        self.walls = []
        self.cannons = []
        self.new_game()

    def new_game(self):
        # add townHall
        self._townHall = TownHall([int(self._height / 2), int(self._width / 2)], self)
        self._scene.add_object(self._townHall)

        # add walls
        town_hall_pos = self._townHall.start_pos
        for i in range(-10, 11):
            self.walls.append(Wall([town_hall_pos[0] - 10, town_hall_pos[1] - i], self))
            self.walls.append(Wall([town_hall_pos[0] + 10, town_hall_pos[1] - i], self))
            self.walls.append(Wall([town_hall_pos[0] - i, town_hall_pos[1] - 10], self))
            self.walls.append(Wall([town_hall_pos[0] - i, town_hall_pos[1] + 10], self))

        for wall in self.walls:
            self._scene.add_object(wall)

        # add cannons

    def handle_input(self):
        inp = input_to(self._input)
        if inp is None:
            return
        if inp in King.KEYS:
            if self.king is None:
                return
            self.king.move(inp)

    def play(self):
        while True:
            self._scene.display()

            while time.time() - self._previous_frame < self._frame_rate:
                pass
            self._previous_frame = time.time()
