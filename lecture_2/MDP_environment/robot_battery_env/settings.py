import pathlib
import pygame
from robot_battery_env.p_matrix import PMatrix

pygame.font.init()

BASE_DIR = pathlib.Path(__file__).parent

# Size of the square tiles used in this environment.
TILE_SIZE = 32

# Size of the dimension NxN
N = 16
# P matrix
P = PMatrix(actions=4, n=N).P

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
H_SCALE = 1
V_SCALE = 1

# Resolution of the actual window
WINDOW_WIDTH = VIRTUAL_WIDTH * H_SCALE 
WINDOW_HEIGHT = VIRTUAL_HEIGHT * V_SCALE

# Default pause time between steps (in seconds)
DEFAULT_DELAY = 0.5

# Textures used in the environment
TEXTURES = {
    'battery': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery.jpeg"),
    'robot': pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot.jpeg"),
    'tile': pygame.image.load(BASE_DIR / "assets" / "graphics" / "tile.jpeg"),
    'level_low_battery': pygame.image.load(BASE_DIR / "assets" / "graphics" / "low_battery.jpeg"),
    'level_mid_battery': pygame.image.load(BASE_DIR / "assets" / "graphics" / "mid_battery.jpeg"),
    'level_full_battery': pygame.image.load(BASE_DIR / "assets" / "graphics" / "full_battery.jpeg"),
    'game_over': pygame.image.load(BASE_DIR / "assets" / "graphics" / "game_over.jpeg"),
    'win': pygame.image.load(BASE_DIR / "assets" / "graphics" / "win.jpeg"),
}

FONTS = {
    'font': pygame.font.Font(BASE_DIR / "assets"/ "fonts" / "font.ttf", 64)
}

GAME_OVER_WIDTH, GAME_OVE_HEIGHT = TEXTURES['game_over'].get_size()
WIN_WIDTH, WIN_HEIGHT = TEXTURES['win'].get_size()
# Initializing the mixer
# pygame.mixer.init()

# # Sound effects
# SOUNDS = {
#     'win': pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "win.ogg")
# }
