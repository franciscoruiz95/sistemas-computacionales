import numpy as np
import random 
import pathlib
import pygame

# Size of the square tiles used in this environment.
TILE_SIZE = 32

# Grid
ROWS = np.random.randint(2, 20)
COLS = np.random.randint(2, 20)


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
    "ice": pygame.image.load(BASE_DIR / "assets" / "graphics" / "ice.png"),
    "hole": pygame.image.load(BASE_DIR / "assets" / "graphics" / "hole.png"),
    "cracked_hole": pygame.image.load(
        BASE_DIR / "assets" / "graphics" / "cracked_hole.png"
    ),
    "goal": pygame.image.load(BASE_DIR / "assets" / "graphics" / "goal.png"),
    "stool": pygame.image.load(BASE_DIR / "assets" / "graphics" / "stool.png"),
    "character": [
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "elf_left.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "elf_down.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "elf_right.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "elf_up.png"),
    ],
    "wall_h": pygame.image.load(BASE_DIR / "assets" / "graphics" / "wall_h.png"),
    "wall_v": pygame.image.load(BASE_DIR / "assets" / "graphics" / "wall_v.png"),
}

# Initializing the mixer
pygame.mixer.init()

# Loading music
pygame.mixer.music.load(BASE_DIR / "assets" / "sounds" / "ice_village.ogg")

# Sound effects
SOUNDS = {
    "ice_cracking": pygame.mixer.Sound(
        BASE_DIR / "assets" / "sounds" / "ice_cracking.ogg"
    ),
    "water_splash": pygame.mixer.Sound(
        BASE_DIR / "assets" / "sounds" / "water_splash.ogg"
    ),
    "win": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "win.ogg"),
}

# Default P matrix
P = {
    0: {
        0: [
            (0.3333333333333333, 0, 0.0, False),
            (0.3333333333333333, 0, 0.0, False),
            (0.3333333333333333, 4, 0.0, False),
        ],
        1: [
            (0.3333333333333333, 0, 0.0, False),
            (0.3333333333333333, 4, 0.0, False),
            (0.3333333333333333, 1, 0.0, False),
        ],
        2: [
            (0.3333333333333333, 4, 0.0, False),
            (0.3333333333333333, 1, 0.0, False),
            (0.3333333333333333, 0, 0.0, False),
        ],
        3: [
            (0.3333333333333333, 1, 0.0, False),
            (0.3333333333333333, 0, 0.0, False),
            (0.3333333333333333, 0, 0.0, False),
        ],
    },
    1: {
        0: [
            (0.3333333333333333, 1, 0.0, False),
            (0.3333333333333333, 0, 0.0, False),
            (0.3333333333333333, 5, 0.0, True),
        ],
        1: [
            (0.3333333333333333, 0, 0.0, False),
            (0.3333333333333333, 5, 0.0, True),
            (0.3333333333333333, 2, 0.0, False),
        ],
        2: [
            (0.3333333333333333, 5, 0.0, True),
            (0.3333333333333333, 2, 0.0, False),
            (0.3333333333333333, 1, 0.0, False),
        ],
        3: [
            (0.3333333333333333, 2, 0.0, False),
            (0.3333333333333333, 1, 0.0, False),
            (0.3333333333333333, 0, 0.0, False),
        ],
    },
    2: {
        0: [
            (0.3333333333333333, 2, 0.0, False),
            (0.3333333333333333, 1, 0.0, False),
            (0.3333333333333333, 6, 0.0, False),
        ],
        1: [
            (0.3333333333333333, 1, 0.0, False),
            (0.3333333333333333, 6, 0.0, False),
            (0.3333333333333333, 3, 0.0, False),
        ],
        2: [
            (0.3333333333333333, 6, 0.0, False),
            (0.3333333333333333, 3, 0.0, False),
            (0.3333333333333333, 2, 0.0, False),
        ],
        3: [
            (0.3333333333333333, 3, 0.0, False),
            (0.3333333333333333, 2, 0.0, False),
            (0.3333333333333333, 1, 0.0, False),
        ],
    },
    3: {
        0: [
            (0.3333333333333333, 3, 0.0, False),
            (0.3333333333333333, 2, 0.0, False),
            (0.3333333333333333, 7, 0.0, True),
        ],
        1: [
            (0.3333333333333333, 2, 0.0, False),
            (0.3333333333333333, 7, 0.0, True),
            (0.3333333333333333, 3, 0.0, False),
        ],
        2: [
            (0.3333333333333333, 7, 0.0, True),
            (0.3333333333333333, 3, 0.0, False),
            (0.3333333333333333, 3, 0.0, False),
        ],
        3: [
            (0.3333333333333333, 3, 0.0, False),
            (0.3333333333333333, 3, 0.0, False),
            (0.3333333333333333, 2, 0.0, False),
        ],
    },
    4: {
        0: [
            (0.3333333333333333, 0, 0.0, False),
            (0.3333333333333333, 4, 0.0, False),
            (0.3333333333333333, 8, 0.0, False),
        ],
        1: [
            (0.3333333333333333, 4, 0.0, False),
            (0.3333333333333333, 8, 0.0, False),
            (0.3333333333333333, 5, 0.0, True),
        ],
        2: [
            (0.3333333333333333, 8, 0.0, False),
            (0.3333333333333333, 5, 0.0, True),
            (0.3333333333333333, 0, 0.0, False),
        ],
        3: [
            (0.3333333333333333, 5, 0.0, True),
            (0.3333333333333333, 0, 0.0, False),
            (0.3333333333333333, 4, 0.0, False),
        ],
    },
    5: {
        0: [(1.0, 5, 0, True)],
        1: [(1.0, 5, 0, True)],
        2: [(1.0, 5, 0, True)],
        3: [(1.0, 5, 0, True)],
    },
    6: {
        0: [
            (0.3333333333333333, 2, 0.0, False),
            (0.3333333333333333, 5, 0.0, True),
            (0.3333333333333333, 10, 0.0, False),
        ],
        1: [
            (0.3333333333333333, 5, 0.0, True),
            (0.3333333333333333, 10, 0.0, False),
            (0.3333333333333333, 7, 0.0, True),
        ],
        2: [
            (0.3333333333333333, 10, 0.0, False),
            (0.3333333333333333, 7, 0.0, True),
            (0.3333333333333333, 2, 0.0, False),
        ],
        3: [
            (0.3333333333333333, 7, 0.0, True),
            (0.3333333333333333, 2, 0.0, False),
            (0.3333333333333333, 5, 0.0, True),
        ],
    },
    7: {
        0: [(1.0, 7, 0, True)],
        1: [(1.0, 7, 0, True)],
        2: [(1.0, 7, 0, True)],
        3: [(1.0, 7, 0, True)],
    },
    8: {
        0: [
            (0.3333333333333333, 4, 0.0, False),
            (0.3333333333333333, 8, 0.0, False),
            (0.3333333333333333, 12, 0.0, True),
        ],
        1: [
            (0.3333333333333333, 8, 0.0, False),
            (0.3333333333333333, 12, 0.0, True),
            (0.3333333333333333, 9, 0.0, False),
        ],
        2: [
            (0.3333333333333333, 12, 0.0, True),
            (0.3333333333333333, 9, 0.0, False),
            (0.3333333333333333, 4, 0.0, False),
        ],
        3: [
            (0.3333333333333333, 9, 0.0, False),
            (0.3333333333333333, 4, 0.0, False),
            (0.3333333333333333, 8, 0.0, False),
        ],
    },
    9: {
        0: [
            (0.3333333333333333, 5, 0.0, True),
            (0.3333333333333333, 8, 0.0, False),
            (0.3333333333333333, 13, 0.0, False),
        ],
        1: [
            (0.3333333333333333, 8, 0.0, False),
            (0.3333333333333333, 13, 0.0, False),
            (0.3333333333333333, 10, 0.0, False),
        ],
        2: [
            (0.3333333333333333, 13, 0.0, False),
            (0.3333333333333333, 10, 0.0, False),
            (0.3333333333333333, 5, 0.0, True),
        ],
        3: [
            (0.3333333333333333, 10, 0.0, False),
            (0.3333333333333333, 5, 0.0, True),
            (0.3333333333333333, 8, 0.0, False),
        ],
    },
    10: {
        0: [
            (0.3333333333333333, 6, 0.0, False),
            (0.3333333333333333, 9, 0.0, False),
            (0.3333333333333333, 14, 0.0, False),
        ],
        1: [
            (0.3333333333333333, 9, 0.0, False),
            (0.3333333333333333, 14, 0.0, False),
            (0.3333333333333333, 11, 0.0, True),
        ],
        2: [
            (0.3333333333333333, 14, 0.0, False),
            (0.3333333333333333, 11, 0.0, True),
            (0.3333333333333333, 6, 0.0, False),
        ],
        3: [
            (0.3333333333333333, 11, 0.0, True),
            (0.3333333333333333, 6, 0.0, False),
            (0.3333333333333333, 9, 0.0, False),
        ],
    },
    11: {
        0: [(1.0, 11, 0, True)],
        1: [(1.0, 11, 0, True)],
        2: [(1.0, 11, 0, True)],
        3: [(1.0, 11, 0, True)],
    },
    12: {
        0: [(1.0, 12, 0, True)],
        1: [(1.0, 12, 0, True)],
        2: [(1.0, 12, 0, True)],
        3: [(1.0, 12, 0, True)],
    },
    13: {
        0: [
            (0.3333333333333333, 9, 0.0, False),
            (0.3333333333333333, 12, 0.0, True),
            (0.3333333333333333, 13, 0.0, False),
        ],
        1: [
            (0.3333333333333333, 12, 0.0, True),
            (0.3333333333333333, 13, 0.0, False),
            (0.3333333333333333, 14, 0.0, False),
        ],
        2: [
            (0.3333333333333333, 13, 0.0, False),
            (0.3333333333333333, 14, 0.0, False),
            (0.3333333333333333, 9, 0.0, False),
        ],
        3: [
            (0.3333333333333333, 14, 0.0, False),
            (0.3333333333333333, 9, 0.0, False),
            (0.3333333333333333, 12, 0.0, True),
        ],
    },
    14: {
        0: [
            (0.3333333333333333, 10, 0.0, False),
            (0.3333333333333333, 13, 0.0, False),
            (0.3333333333333333, 14, 0.0, False),
        ],
        1: [
            (0.3333333333333333, 13, 0.0, False),
            (0.3333333333333333, 14, 0.0, False),
            (0.3333333333333333, 15, 1.0, True),
        ],
        2: [
            (0.3333333333333333, 14, 0.0, False),
            (0.3333333333333333, 15, 1.0, True),
            (0.3333333333333333, 10, 0.0, False),
        ],
        3: [
            (0.3333333333333333, 15, 1.0, True),
            (0.3333333333333333, 10, 0.0, False),
            (0.3333333333333333, 13, 0.0, False),
        ],
    },
    15: {
        0: [(1.0, 15, 0, True)],
        1: [(1.0, 15, 0, True)],
        2: [(1.0, 15, 0, True)],
        3: [(1.0, 15, 0, True)],
    },
}
