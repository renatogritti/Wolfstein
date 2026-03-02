import math
from .config import *

"""
Configurações do Jogo (Settings)
Este arquivo contém todas as constantes e configurações globais do jogo/engine.
"""

# Configurações do Jogo
RES = WIDTH, HEIGHT = 1600, 900
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

# Player settings
PLAYER_POS = 1.5, 5 # mini_map
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002

# Raycasting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

# Screen distance
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
TEXTURE_SIZE = 128
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
SCALE = WIDTH // NUM_RAYS

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (110, 110, 110)
YELLOW = (220, 220, 0)
GREEN = (0, 200, 0)
