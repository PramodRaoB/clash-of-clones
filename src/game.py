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
from src.buildings.wizard_tower import WizardTower
from src.characters.king import King
from src.characters.queen import Queen
from src.spells.heal import Heal
from src.spells.rage import Rage
from src.spells.spell import Spell
from src.input import Get
from src.scene import Scene
from src.input import input_to

from src.utils import wait, play_audio


class Game:
    def __init__(self, playerType: int):
        self.gameType = playerType
        # check if current terminal size is sufficient for the game
        self.player = None
        self.townHall = None
        term_sz = os.get_terminal_size()
        if term_sz.lines < conf.GAME_HEIGHT or term_sz.columns < conf.GAME_WIDTH:
            print(f"{Fore.RED}{Back.BLACK}{Style.BRIGHT}Increase terminal window size to continue")
            sys.exit(1)

        self._height = conf.GAME_HEIGHT
        self._width = conf.GAME_WIDTH
        self.size = np.array([self._height, self._width])
        self._input = Get()

        self.scene = Scene(self.size)
        self._frame_rate = 1 / 30
        self._previous_frame = time.time()
        self.walls = []
        self.cannons = []
        self.wizards = []
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
        self._barbs = 0
        self._archers = 0
        self._balloons = 0
        self._rages = 0
        self._heals = 0

        self.curr_level = 1
        self.new_game(1)

    def new_game(self, ind: int):
        # init
        self.scene = Scene(self.size)
        self._frame_rate = 1 / 30
        self._previous_frame = time.time()
        self.walls = []
        self.cannons = []
        self.wizards = []
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
        self._barbs = 0
        self._archers = 0
        self._balloons = 0
        self._rages = 0
        self._heals = 0
        os.system("pkill mpg123")
        if ind == 1:
            import src.levels.level1 as lvl
        elif ind == 2:
            import src.levels.level2 as lvl
        else:
            import src.levels.level3 as lvl

        # add townHall
        self.townHall = TownHall(np.array(lvl.TOWNHALL), self)
        self.scene.add_object(self.townHall)
        self.buildings.append(self.townHall)

        # add walls
        for i in lvl.WALLS:
            self.walls.append(Wall(np.array(i), self))

        # add huts
        for i in lvl.HUTS:
            self.buildings.append(Hut(np.array(i), self))

        # add cannons
        for i in lvl.CANNONS:
            self.cannons.append(Cannon(np.array(i), self))

        # add wizard tower
        for i in lvl.WIZARDS:
            self.wizards.append(WizardTower(np.array(i), self))

        for cannon in self.cannons:
            self.buildings.append(cannon)
        for wizard in self.wizards:
            self.buildings.append(wizard)

        # add spawners
        for i in lvl.BARB_SPAWNERS:
            self.spawners.append(BarbSpawner(np.array(i), self))
        for i in lvl.ARCHER_SPAWNERS:
            self.spawners.append(ArcherSpawner(np.array(i), self))
        for i in lvl.BALLOON_SPAWNERS:
            self.spawners.append(BalloonSpawner(np.array(i), self))

        # add king
        self.player = Queen(np.array([0, 0]), self)
        if self.gameType == 1:
            self.player = Queen(np.array([0, 0]), self)
        elif self.gameType == 2:
            self.player = King(np.array([0, 0]), self)
        else:
            sys.exit(1)
        self.characters.append(self.player)

        self.curr_level = ind
        play_audio("src/assets/intro.mp3")
        play_audio("src/assets/theme.mp3")

    def handle_input(self):
        inp = input_to(self._input, self._frame_rate)
        if inp is None:
            return
        if inp in King.KEYS:
            if self.player is None:
                return
            if inp == ' ':
                self.player.attack()
            else:
                self.player.move(inp)

        if inp in Spawner.KEYS:
            if inp in BarbSpawner.KEYS and self._barbs == conf.BARB_LIMIT * self.curr_level:
                return
            elif inp in ArcherSpawner.KEYS and self._archers == conf.ARCHER_LIMIT * self.curr_level:
                return
            elif inp in BalloonSpawner.KEYS and self._balloons == conf.BALLOON_LIMIT * self.curr_level:
                return
            if self.spawners[int(inp) - int("1")].update():
                if inp in BarbSpawner.KEYS:
                    self._barbs += 1
                elif inp in ArcherSpawner.KEYS:
                    self._archers += 1
                else:
                    self._balloons += 1

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

        if inp == 'e' and self.gameType == 1:
            if not self.player.use_eagle:
                self.player.use_eagle = True
                self.player.use_eagle_time = time.time()

        if inp == 'q':
            self.over = True
            time.sleep(2)
            self.scene.game_over(False, self._score, int(time.time() - self._start_time), self._barbs, self._archers,
                                 self._balloons, self._rages, self._heals)

    def prune_dead(self):
        if self.townHall is not None and self.townHall.is_dead():
            self.buildings.remove(self.townHall)
            self.townHall = None
            self._score += conf.TOWNHALL_SCORE

        if self.player is not None and self.player.is_dead():
            self.characters.remove(self.player)
            self.player = None

        for cannon in self.cannons:
            if cannon is not None and cannon.is_dead():
                self.buildings.remove(cannon)
                self.cannons.remove(cannon)
                self._score += conf.CANNON_SCORE

        for wizard in self.wizards:
            if wizard is not None and wizard.is_dead():
                self.buildings.remove(wizard)
                self.wizards.remove(wizard)
                self._score += conf.WIZARD_SCORE

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

    def get_character_on_coord(self, coords: ndarray):
        ret = []
        for c in self.characters:
            if c is not None and not c.is_dead() and c.is_intersecting(coords):
                ret.append(c)

        return ret

    def update_alive(self):
        if self.gameType == 1 and self.player is not None:
            # if queen
            if self.player.use_eagle and not wait(self.player.use_eagle_time, conf.EAGLE_DELAY):
                if self.player.eagle():
                    self.player.use_eagle = False


        for barb in self.barbs:
            if barb is not None and not barb.is_dead():
                barb.update()

        for cannon in self.cannons:
            cannon.update()

        for wizard in self.wizards:
            wizard.update()

        for spell in self.active_spells:
            spell.update()

    def check_game_over(self):
        if len(self.buildings) == 0:
            self.over = True
            time.sleep(2)
            if self.curr_level <= 2:
                self.new_game(self.curr_level + 1)
            else:
                self.scene.game_over(True, self._score, int(time.time() - self._start_time), self._barbs, self._archers,
                                     self._balloons, self._rages, self._heals)
        elif len(self.characters) == 0:
            self.over = True
            time.sleep(2)
            self.scene.game_over(False, self._score, int(time.time() - self._start_time), self._barbs, self._archers,
                                 self._balloons, self._rages, self._heals)

    def play(self):
        while not self.over:
            # Game logic
            self.handle_input()
            if not self.over:
                self.prune_dead()
                self.update_alive()

                # Render objects
                self.scene.clear()
                if self.player is not None:
                    self.scene.hud(self._score, int(time.time() - self._start_time), self._barbs, self._archers,
                                   self._balloons, self._rages,
                                   self._heals, self.player.health, self.player.max_health)
                else:
                    self.scene.hud(self._score, int(time.time() - self._start_time), self._barbs, self._archers,
                                   self._balloons, self._rages, self._heals)
                self.render()
                self.scene.display()

                self.check_game_over()

                while time.time() - self._previous_frame < self._frame_rate:
                    pass
                self._previous_frame = time.time()
