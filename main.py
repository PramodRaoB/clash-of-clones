import os

from game import Game

if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

game = Game()
game.play()