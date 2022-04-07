import numpy as np
from colorama import Fore, Back, Style

GAME_WIDTH = 150
GAME_HEIGHT = 40

BG_COLOUR = Back.BLACK
RAGE_COLOUR = Back.MAGENTA
HEAL_COLOUR = Back.GREEN

HEALTH0 = Fore.GREEN
HEALTH1 = Fore.YELLOW
HEALTH2 = Fore.RED

CANNON0 = Back.BLACK
CANNON1 = Back.RED

CHAR_HEALTH0 = Fore.WHITE
CHAR_HEALTH1 = Fore.LIGHTGREEN_EX
CHAR_HEALTH2 = Fore.LIGHTYELLOW_EX
CHAR_HEALTH3 = Fore.LIGHTRED_EX
CHAR_HEALTH4 = Fore.LIGHTBLACK_EX

# height, width
TOWNHALL_SIZE = np.array([4, 3])
HUT_SIZE = np.array([3, 3])
CANNON_SIZE = np.array([2, 2])
WALL_SIZE = np.array([1, 1])
SPAWNER_SIZE = np.array([1, 1])

# hp
TOWNHALL_HP = 500
HUT_HP = 250
CANNON_HP = 75
WALL_HP = 100
KING_HP = 100
BARB_HP = 76
ARCHER_HP = BARB_HP / 2
BALLOON_HP = BARB_HP

# damage
KING_DAMAGE = 30
CANNON_DAMAGE = 5
BARB_DAMAGE = 16
ARCHER_DAMAGE = BARB_DAMAGE / 2
BALLOON_DAMAGE = BARB_DAMAGE * 2

# movement speed
KING_SPEED = 0.05
BARB_SPEED = 0.03
ARCHER_SPEED = BARB_SPEED * 2
BALLOON_SPEED = BARB_SPEED * 2

KING_RADIUS = 3
CANNON_RADIUS = 20
ARCHER_RADIUS = CANNON_RADIUS + 5

BARB_COOLDOWN = 2
ARCHER_COOLDOWN = 2
BALLOON_COOLDOWN = 4
KING_COOLDOWN = 1
CANNON_COOLDOWN = 1.5
SPAWNER_COOLDOWN = 5

RAGE_DURATION = 5
HEAL_FACTOR = 1.5
RAGE_FACTOR = 2
RAGE_COOLDOWN = 5
HEAL_COOLDOWN = 7

# scores
TOWNHALL_SCORE = 1000
CANNON_SCORE = 100
WALL_SCORE = 10
HUT_SCORE = 50

# Troop limits
BARB_LIMIT = 6
ARCHER_LIMIT = 6
BALLOON_LIMIT = 3
