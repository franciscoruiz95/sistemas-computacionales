"""
ISPTSC 2023
Lecture 1

Author: Alejandro Mujica - alejandro.j.mujic4@gmail.com
Author: Jesús Pérez - perezj89@gmail.com

This file contains the the Two-Armed Bandit Environment.
"""
import time

import gym

import numpy as np

import pygame

from . import settings

pygame.init()
pygame.display.init()

class Arm:
    def __init__(self, p=0, earn=0):
        self.probability = p
        self.earn = earn
    
    def pull(self):
        return self.earn if np.random.random() < self.probability else 0

    def __str__(self):
        return f"Arm: p = {self.probability}, earn: {self.earn}"
    
    def __repr__(self):
        return f"Arm: p = {self.probability}, earn: {self.earn}"


class TwoArmedBanditEnv(gym.Env):
    

    def __init__(self):
        self.arms = (
            Arm(0.5, 1),
            Arm(0.1, 100)
        )
        self.action = None
        self.reward = None
        self.observation_space = gym.spaces.Discrete(1)
        self.action_space = gym.spaces.Discrete(len(self.arms))

        self.window = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Two-Armed Bandit Environment")        

    def _get_observations(self):
        return 0

    def _get_info(self):
        return { 'state': 0 }

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        return self._get_observations(), self._get_info()

    def step(self, action):
        self.action = action
        self.reward = self.arms[action].pull()
        self.render()
        return self._get_observations(), self.reward, False, False, self._get_info()

    def render(self):
        self.window.fill((255, 255, 255))

        # Render the first machine
        self.window.blit(settings.TEXTURES['machine'], (50, 100))

        # Render the second machine
        self.window.blit(settings.TEXTURES['machine'], (100 + settings.MACHINE_WIDTH, 100))

        # Render the arrow under the selected machine
        x = 50 + settings.MACHINE_WIDTH / 2

        if self.action == 1:
            x += settings.MACHINE_WIDTH + 50

        y = settings.WINDOW_HEIGHT - 50 - settings.ARROW_HEIGHT / 2
        self.window.blit(settings.TEXTURES['arrow'], (x - settings.ARROW_WIDTH / 2 - 80, y))

        # Render the reward
        text_obj = settings.FONTS['font'].render(f"{self.reward}", True, (0, 0, 0))
        text_rect = text_obj.get_rect()
        text_rect.center = (x + 2, 52)
        self.window.blit(text_obj, text_rect)
        text_obj = settings.FONTS['font'].render(f"{self.reward}", True, (255, 250, 26))
        text_rect = text_obj.get_rect()
        text_rect.center = (x, 50)
        self.window.blit(text_obj, text_rect)

        pygame.event.pump()
        pygame.display.update()

        time.sleep(0.5)

    def close(self):
        pygame.display.quit()
        pygame.font.quit()
        pygame.quit()
