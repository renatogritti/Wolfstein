import sys
import os

# Ensure the src directory is in the path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.game import Game

if __name__ == '__main__':
    game = Game()
    game.run()
