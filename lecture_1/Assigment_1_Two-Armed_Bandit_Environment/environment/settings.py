"""
ISPTSC 2023
Lecture 1

Author: Alejandro Mujica - alejandro.j.mujic4@gmail.com
Author: Jesús Pérez - perezj89@gmail.com

This file contains constans to define the environment.
"""
import pathlib

import pygame

BASE_DIR = pathlib.Path(__file__).parent

TEXTURES = {
    'machine': pygame.image.load(BASE_DIR / "assets"/ "graphics" / "slot-machine.png"),
    'arrow': pygame.image.load(BASE_DIR / "assets"/ "graphics" / "up_arrow.png"),
}

pygame.font.init()

FONTS = {
    'font': pygame.font.Font(BASE_DIR / "assets"/ "fonts" / "font.ttf", 64)
} 

ARROW_WIDTH, ARROW_HEIGHT = TEXTURES['arrow'].get_size()
MACHINE_WIDTH, MACHINE_HEIGHT = TEXTURES['machine'].get_size()
WINDOW_WIDTH = MACHINE_WIDTH * 2 + 150
WINDOW_HEIGHT = 200 + MACHINE_HEIGHT
