import os
import sys
import time

import numpy as np
from numpy import ndarray

import src.config as conf
from colorama import Fore, Back, Style

from src.buildings.cannon import Cannon
from src.buildings.hut import Hut
from src.buildings.barb_spawner import BarbSpawner
from src.buildings.archer_spawner import ArcherSpawner
from src.buildings.balloon_spawner import BalloonSpawner
from src.buildings.spawner import Spawner
from src.buildings.townhall import TownHall
from src.buildings.wall import Wall
from src.characters.king import King
from src.spells.heal import Heal
from src.spells.rage import Rage
from src.spells.spell import Spell
from src.input import Get
from src.scene import Scene
from src.input import input_to

from src.utils import wait, play_audio


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

        self._frame_rate = 1 / 30
        self._previous_frame = time.time()
        self.walls = []
        self.cannons = []
        self.buildings = []
        self.barbs = []
        self.characters = []
        self.spawners = []
        self.last_rage = 0
        self.last_heal = 0
        self.active_spells = []
        self.last_theme = time.time()

        self.over = False
        self._score = 0
        self._start_time = time.time()
        self._troops = 0
        self._rages = 0
        self._heals = 0

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
        for i in range(-9, 10):
            self.walls.append(Wall(np.array([town_hall_pos[0] - i, town_hall_pos[1] - 10]), self))
            self.walls.append(Wall(np.array([town_hall_pos[0] - i, town_hall_pos[1] + 10]), self))

        self.buildings.append(Hut(np.array([int(self._height / 4), int(self._width / 4)]), self))
        self.buildings.append(Hut(np.array([int(self._height / 4), int(3 * self._width / 4)]), self))
        self.buildings.append(Hut(np.array([int(3 * self._height / 4), int(self._width / 4)]), self))
        self.buildings.append(Hut(np.array([int(3 * self._height / 4), int(3 * self._width / 4)]), self))
        self.buildings.append(Hut(np.array([town_hall_pos[0] - 5, town_hall_pos[1] + 3]), self))

        self.cannons.append(Cannon(np.array([town_hall_pos[0] - 7, town_hall_pos[1] + 7]), self))
        self.cannons.append(Cannon(np.array([30, 20]), self))
        self.cannons.append(Cannon(np.array([self.size[0] - 10, self.size[1] - 10]), self))

        self.spawners.append(BalloonSpawner(np.array([10, 10]), self))
        self.spawners.append(BalloonSpawner(np.array([25, 140]), self))
        self.spawners.append(BalloonSpawner(np.array([30, 100]), self))

        self.buildings.append(self.townHall)
        for cannon in self.cannons:
            self.buildings.append(cannon)

        # add king
        self.king = King(np.array([0, 0]), self)
        self.characters.append(self.king)

        play_audio("src/assets/intro.mp3")
        play_audio("src/assets/theme.mp3")

    def handle_input(self):
        inp = input_to(self._input, self._frame_rate)
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
            if self.spawners[int(inp) - int("1")].update():
                self._troops += 1

        if inp in Spell.KEYS:
            if inp == 'r':
                if not wait(self.last_rage, conf.RAGE_COOLDOWN):
                    self.last_rage = time.time()
                    self.active_spells.append(Rage(self))
                    self._rages += 1
            else:
                if not wait(self.last_heal, conf.HEAL_COOLDOWN):
                    self.last_heal = time.time()
                    Heal(self)
                    self._heals += 1

        if inp == 'q':
            self.over = True
            time.sleep(2)
            self.scene.game_over(False, self._score, int(time.time() - self._start_time), self._troops, self._rages,
                                 self._heals)

    def prune_dead(self):
        if self.townHall is not None and self.townHall.is_dead():
            self.buildings.remove(self.townHall)
            self.townHall = None
            self._score += conf.TOWNHALL_SCORE

        if self.king is not None and self.king.is_dead():
            self.characters.remove(self.king)
            self.king = None

        for cannon in self.cannons:
            if cannon is not None and cannon.is_dead():
                self.buildings.remove(cannon)
                self.cannons.remove(cannon)
                self._score += conf.CANNON_SCORE

        for wall in self.walls:
            if wall is not None and wall.is_dead():
                self.walls.remove(wall)
                self._score += conf.WALL_SCORE

        for barb in self.barbs:
            if barb is not None and barb.is_dead():
                self.characters.remove(barb)
                self.barbs.remove(barb)

        for building in self.buildings:
            if building is not None and building.is_dead():
                self.buildings.remove(building)

        for c in self.characters:
            if c is not None and c.is_dead():
                self.characters.remove(c)

        for spell in self.active_spells:
            if spell is not None and spell.is_over:
                self.active_spells.remove(spell)

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

        for spell in self.active_spells:
            spell.update()

    def check_game_over(self):
        if len(self.buildings) == 0:
            self.over = True
            time.sleep(2)
            self.scene.game_over(True, self._score, int(time.time() - self._start_time), self._troops, self._rages,
                                 self._heals)
        elif len(self.characters) == 0:
            self.over = True
            time.sleep(2)
            self.scene.game_over(False, self._score, int(time.time() - self._start_time), self._troops, self._rages,
                                 self._heals)

    def play(self):
        while not self.over:
            # Game logic
            self.handle_input()
            if time.time() - self.last_theme > 180:
                play_audio("src/assets/theme.mp3")
            if not self.over:
                self.prune_dead()
                self.update_alive()

                # Render objects
                self.scene.clear()
                if self.king is not None:
                    self.scene.hud(self._score, int(time.time() - self._start_time), self._troops, self._rages,
                                   self._heals, self.king.health, self.king.max_health)
                else:
                    self.scene.hud(self._score, int(time.time() - self._start_time), self._troops, self._rages,
                                   self._heals)
                self.render()
                self.scene.display()

                self.check_game_over()

                while time.time() - self._previous_frame < self._frame_rate:
                    pass
                self._previous_frame = time.time()
