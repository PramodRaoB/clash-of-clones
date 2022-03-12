import os
import sys
import time

import numpy as np
from numpy import ndarray

import config as conf
from colorama import Fore, Back, Style

from buildings.cannon import Cannon
from buildings.hut import Hut
from buildings.spawner import Spawner
from buildings.townhall import TownHall
from buildings.wall import Wall
from characters.barbarian import Barbarian
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

        self._frame_rate = 1 / 20
        self._previous_frame = time.time()
        self.walls = []
        self.cannons = []
        self.buildings = []
        self.barbs = []
        self.characters = []
        self.spawners = []

        self.over = False
        self._score = 0
        self._start_time = time.time()
        self._troops = 0
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

        self.buildings.append(Hut(np.array([int(self._height / 4), int(self._width / 4)]), self))
        self.buildings.append(Hut(np.array([int(self._height / 4), int(3 * self._width / 4)]), self))
        self.buildings.append(Hut(np.array([int(3 * self._height / 4), int(self._width / 4)]), self))
        self.buildings.append(Hut(np.array([int(3 * self._height / 4), int(3 * self._width / 4)]), self))
        self.buildings.append(Hut(np.array([town_hall_pos[0] - 5, town_hall_pos[1] + 3]), self))

        self.cannons.append(Cannon(np.array([town_hall_pos[0] - 7, town_hall_pos[1] + 7]), self))

        # TODO: add others
        self.spawners.append(Spawner(np.array([10, 10]), self))
        self.spawners.append(Spawner(np.array([25, 140]), self))
        self.spawners.append(Spawner(np.array([40, 100]), self))

        self.buildings.append(self.townHall)
        for cannon in self.cannons:
            self.buildings.append(cannon)

        # add king
        self.king = King(np.array([0, 0]), self)
        self.characters.append(self.king)

    def handle_input(self):
        inp = input_to(self._input)
        if inp is None:
            return
        if inp in King.KEYS:
            if self.king is None:
                return
            if inp == ' ':
                self.king.attack()
            else:
                self.king.move(inp)

        if inp in Spawner.KEYS:
            self.spawners[int(inp) - int("1")].update()

        if inp == 'q':
            sys.exit(0)

    def prune_dead(self):
        if self.townHall is not None and self.townHall.is_dead():
            self.buildings.remove(self.townHall)
            self.townHall = None

        if self.king is not None and self.king.is_dead():
            self.characters.remove(self.king)
            self.king = None

        for building in self.buildings:
            if building is not None and building.is_dead():
                self.buildings.remove(building)

        for wall in self.walls:
            if wall is not None and wall.is_dead():
                self.walls.remove(wall)

        for c in self.characters:
            if c is not None and c.is_dead():
                self.characters.remove(c)

    def render(self):
        for spawner in self.spawners:
            self.scene.add_object(spawner)

        for building in self.buildings:
            self.scene.add_object(building)

        for wall in self.walls:
            self.scene.add_object(wall)

        for c in self.characters:
            self.scene.add_object(c)

    def get_structure_on_coord(self, coords: ndarray):
        # check walls
        for wall in self.walls:
            if wall is not None and not wall.is_dead() and wall.is_intersecting(coords):
                return wall

        for building in self.buildings:
            if building is not None and not building.is_dead() and building.is_intersecting(coords):
                return building

        return None

    def update_alive(self):
        for barb in self.barbs:
            if barb is not None and not barb.is_dead():
                barb.update()

        for cannon in self.cannons:
            cannon.update()

    def check_game_over(self):
        if len(self.buildings) == 0:
            self.over = True
            time.sleep(2)
            self.scene.game_over(True, self._score, int(time.time() - self._start_time), self._troops)
        elif len(self.characters) == 0:
            self.over = True
            time.sleep(2)
            self.scene.game_over(False, self._score, int(time.time() - self._start_time), self._troops)
        print(f"{len(self.buildings)} and {len(self.characters)}")

    def play(self):
        while not self.over:
            # Game logic
            self.handle_input()
            self.prune_dead()
            self.update_alive()

            # Render objects
            self.scene.clear()
            self.render()
            self.scene.display()

            self.check_game_over()

            while time.time() - self._previous_frame < self._frame_rate:
                pass
            self._previous_frame = time.time()
