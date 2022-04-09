import os

from src.game import Game

print("Welcome to Clash of Clones")
print("Input 1 for Queen and 2 for King: ")
playerType = int(input())

if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

game = Game(playerType)
game.play()
