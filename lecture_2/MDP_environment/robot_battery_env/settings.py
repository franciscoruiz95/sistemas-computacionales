import pathlib
import pprint
import pygame
from p_matrix import P

# Size of the square tiles used in this environment.
TILE_SIZE = 32

# Size of the dimension NxN
N = 16
# P matrix
P = P(actions=4, n=N).P

# Grid
ROWS = N
COLS = N

NUM_TILES = ROWS * COLS
NUM_ACTIONS = 4
INITIAL_STATE = 0

# Resolution to emulate
VIRTUAL_WIDTH = TILE_SIZE * COLS
VIRTUAL_HEIGHT = TILE_SIZE * ROWS

# Scale factor between virtual screen and window
H_SCALE = 4
V_SCALE = 4

# Resolution of the actual window
WINDOW_WIDTH = VIRTUAL_WIDTH * H_SCALE
WINDOW_HEIGHT = VIRTUAL_HEIGHT * V_SCALE

# Default pause time between steps (in seconds)
DEFAULT_DELAY = 0.5

BASE_DIR = pathlib.Path(__file__).parent

# Textures used in the environment
TEXTURES = {
    'battery': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery.jpeg"),
    'robot': pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot.jpeg"),
    'tile': pygame.image.load(BASE_DIR / "assets" / "graphics" / "tile.jpeg"),
}

# Initializing the mixer
pygame.mixer.init()

# Sound effects
SOUNDS = {
    'win': pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "win.ogg")
}
