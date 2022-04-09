"""
.....................................................................................................................................................
.....................................................................................................................................................
...........z.........................................................................................................................................
.....................................................................................................................................................
..........................................HHH........................................................................................................
..........................................HHH.....................................................................z..................................
..........................................HHH........................................................................................................
.....................................................................................................................................................
.........................................................................x...........................................................................
.....................................................................................................................................................
.....................................................................................................................................................
.....................................................................................................................................................
.....................................................................................................................................................
....................................................................................WWW..............................................................
................................HHH..........................WWW....................WWW......HHH.....................................................
................................HHH..........................WWW....................WWW......HHH.....................................................
................................HHH..........................WWW.............................HHH.....................................................
.......................................{{................###########.................................................................................
.......................................{{...............#...........#................................................................................
..............................................######...#........{{...#...######......................................................................
.............................................#......#.#.........{{....#.#......#.....................................................................
............................................#....WWW.#.......TTT.......#.WWW....#............................y.......................................
............x...............................#....WWW.#.......TTT.......#.WWW....#....................................................................
............................................#....WWW.#.......TTT.......#.WWW....#....................................................................
................y...........................#..{{....#.......TTT.......#....{{..#............HHH.....................................................
.............................................#.{{...#.#....{{.........#.#...{{.#.............HHH.....................................................
..............................................######...#...{{........#...######..............HHH.....................................................
........................................................#...........#................................................................................
.........................................................###########.................................................................................
....................................HHH......................WWW.....................................................................................
....................................HHH......................WWW.............{{..............................x.......................................
....................................HHH......................WWW.............{{......................................................................
.....................................................................................................................................................
.....................................................................................................................................................
.....................................................................................................................................................
.....................................................................................................................................................
.....................................................................................................................................................
.....................................................................................................................................................
.....................................z.............................................y.................................................................
.....................................................................................................................................................
"""
import sys

level_design = [
    ".....................................................................................................................................................",
    ".....................................................................................................................................................",
    "...........z.........................................................................................................................................",
    ".....................................................................................................................................................",
    "..........................................HHH........................................................................................................",
    "..........................................HHH.....................................................................z..................................",
    "..........................................HHH........................................................................................................",
    ".....................................................................................................................................................",
    ".........................................................................x...........................................................................",
    ".....................................................................................................................................................",
    ".....................................................................................................................................................",
    ".....................................................................................................................................................",
    ".....................................................................................................................................................",
    "....................................................................................WWW..............................................................",
    "................................HHH..........................WWW....................WWW......HHH.....................................................",
    "................................HHH..........................WWW....................WWW......HHH.....................................................",
    "................................HHH..........................WWW.............................HHH.....................................................",
    ".......................................{{................###########.................................................................................",
    ".......................................{{...............#...........#................................................................................",
    "..............................................######...#........{{...#...######......................................................................",
    ".............................................#......#.#.........{{....#.#......#.....................................................................",
    "............................................#....WWW.#.......TTT.......#.WWW....#............................y.......................................",
    "............x...............................#....WWW.#.......TTT.......#.WWW....#....................................................................",
    "............................................#....WWW.#.......TTT.......#.WWW....#....................................................................",
    "................y...........................#..{{....#.......TTT.......#....{{..#............HHH.....................................................",
    ".............................................#.{{...#.#....{{.........#.#...{{.#.............HHH.....................................................",
    "..............................................######...#...{{........#...######..............HHH.....................................................",
    "........................................................#...........#................................................................................",
    ".........................................................###########.................................................................................",
    "....................................HHH......................WWW.....................................................................................",
    "....................................HHH......................WWW.............{{..............................x.......................................",
    "....................................HHH......................WWW.............{{......................................................................",
    ".....................................................................................................................................................",
    ".....................................................................................................................................................",
    ".....................................................................................................................................................",
    ".....................................................................................................................................................",
    ".....................................................................................................................................................",
    ".....................................................................................................................................................",
    ".....................................z.............................................y.................................................................",
    ".....................................................................................................................................................",
]

# add walls
WALLS = []

# add huts
HUTS = []

# add cannons
CANNONS = []

# add wizards
WIZARDS = []

# add spawners
# barb, archer, balloon
BARB_SPAWNERS = []
ARCHER_SPAWNERS = []
BALLOON_SPAWNERS = []


def is_top_left(coord):
    new_c = [[coord[0] - 1, coord[1]], [coord[0] - 1, coord[1] - 1], [coord[0], coord[1] - 1]]
    for test_c in new_c:
        if test_c[0] < 0 or test_c[1] < 0 or test_c[0] >= len(level_design) or test_c[1] >= len(level_design[0]):
            continue
        if level_design[test_c[0]][test_c[1]] == level_design[coord[0]][coord[1]]:
            return False

    return True


for i in range(len(level_design)):
    for j in range(len(level_design[0])):
        if level_design[i][j] == '.':
            continue
        if level_design[i][j] == "#":
            WALLS.append([i, j])
        elif level_design[i][j] == 'x':
            BARB_SPAWNERS.append([i, j])
        elif level_design[i][j] == 'y':
            ARCHER_SPAWNERS.append([i, j])
        elif level_design[i][j] == 'z':
            BALLOON_SPAWNERS.append([i, j])
        else:
            if not is_top_left([i, j]):
                continue
            if level_design[i][j] == 'T':
                TOWNHALL = [i, j]
            elif level_design[i][j] == 'H':
                HUTS.append([i, j])
            elif level_design[i][j] == '{':
                CANNONS.append([i, j])
            elif level_design[i][j] == 'W':
                WIZARDS.append([i, j])