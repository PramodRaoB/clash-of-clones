# clash-of-clones
A terminal python game which takes heavy inspiration from the game clash of clans

## Entities
- `P`: Represents the King controlled by the player
- `!`: Represents the Barbarian (your ally)
- `W`: Represents a wall
- `H`: Represents a pixel of the hut
- `{`: Represents a pixel of the cannon
- `x`: Represents a spawner for the Barbarians
- `T`: Represents a pixel of the townHall

## Controls
- `w`, `s`, `a`, `d`: To move the king Up, Down, Left and Right respectively
- `space`: To perform an AoE (Leviathan Axe)
- `1`, `2`, `3`: Spawns a barbarian at one of the pre-defined spawners
- `r`: Deploy rage spell (Movement speed and damage of all troops)
- `h`: Deploy heal spell (Every troops health is increased to 1.5x but capped at their maximum health)
- `q`: Quits the game

## Instructions to install

1. Navigate to the repository
   `cd /pat/to/repository`
2. Install the required packages
   `pip3 install -r requirements.txt`
3. Enjoy! :D
   `python3 main.py`

## Replays!
You can now watch replays for your gameplay.
Simply play a game and then run,

`python3 replay.py replays/replay_name`
