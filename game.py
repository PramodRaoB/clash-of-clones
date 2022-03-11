import os
import sys
import time

import numpy as np

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
        self.king = None
        self.townHall = None
        term_sz = os.get_terminal_size()
        if term_sz.lines < conf.GAME_HEIGHT or term_sz.columns < conf.GAME_WIDTH:
            print(f"{Fore.RED}{Back.BLACK}{Style.BRIGHT}Increase terminal window size to continue")
            sys.exit(1)

        self._height = conf.GAME_HEIGHT
        self._width = conf.GAME_WIDTH
        self.size = np.array([self._height, self._width])
        self.scene = Scene(self.size)
        self._input = Get()

        self._frame_rate = 1 / 60
        self._previous_frame = time.time()
        self.walls = []
        self.cannons = []
        self.new_game()

    def new_game(self):
        # add townHall
        self.townHall = TownHall(np.array([int(self._height / 2), int(self._width / 2)]), self)
        self.scene.add_object(self.townHall)

        # add walls
        town_hall_pos = self.townHall.start_pos
        for i in range(-10, 11):
            self.walls.append(Wall(np.array([town_hall_pos[0] - 10, town_hall_pos[1] - i]), self))
            self.walls.append(Wall(np.array([town_hall_pos[0] + 10, town_hall_pos[1] - i]), self))
            self.walls.append(Wall(np.array([town_hall_pos[0] - i, town_hall_pos[1] - 10]), self))
            self.walls.append(Wall(np.array([town_hall_pos[0] - i, town_hall_pos[1] + 10]), self))

        for wall in self.walls:
            self.scene.add_object(wall)

        # add cannons

        # add king
        self.king = King(np.array([0, 0]), self)

    def handle_input(self):
        inp = input_to(self._input)
        if inp is None:
            return
        if inp in King.KEYS:
            if self.king is None:
                return
            if inp == ' ':
                pass
            else:
                self.king.move(inp)
        if inp == 'q':
            sys.exit(0)

    def render(self):
        if self.townHall is not None:
            self.scene.add_object(self.townHall)

        for wall in self.walls:
            if wall is not None:
                self.scene.add_object(wall)

        if self.king is not None:
            self.scene.add_object(self.king)

    def play(self):
        while True:
            # Game logic
            self.handle_input()

            # Render objects
            self.scene.clear()
            self.render()
            self.scene.display()

            while time.time() - self._previous_frame < self._frame_rate:
                pass
            self._previous_frame = time.time()
