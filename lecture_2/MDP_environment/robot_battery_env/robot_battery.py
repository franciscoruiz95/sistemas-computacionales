import time

import numpy as np

import gym
from gym import spaces
import pygame

from . import settings
from .world import World


class RobotBattery(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, **kwargs):
        super().__init__()
        self.observation_space = spaces.Discrete(settings.NUM_TILES)
        self.action_space = spaces.Discrete(settings.NUM_ACTIONS)
        self.current_action = 1
        self.current_state = 0
        self.current_reward = 0.0
        self.delay = settings.DEFAULT_DELAY
        self.P = settings.P
        self.initial_energy = 100.0
        self.current_energy = self.initial_energy
        self.world = World(
            "Robot Battery Environment",
            self.current_state,
            self.current_action,
            self.initial_energy
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get('delay', 0.5)

        np.random.seed(seed)
        self.current_state = 0
        self.current_action = 1
        self.world.reset(self.current_state, self.current_action)
        return 0, {}

    def step(self, action):

        truncated = False

        if np.random.random() < 1 - self.current_energy / self.initial_energy:
            random_action = np.random.random_integers(0, 3)
            print(random_action, self.current_energy, self.current_state)
            self.current_action = random_action
            prob = self.P[self.current_state][self.current_action]

        # Elegir quedarse en la misma posición o ir a una diferente a la elegida por la acción
        else:
            # Ir a la dirección esperada por la acción
            print(self.current_action, self.current_energy, self.current_state)
            self.current_action = action
            prob = self.P[self.current_state][self.current_action]

        p, self.current_state, self.current_reward, terminated = prob[0]

        self.current_energy -= 2 * 0.7

        if self.current_energy <= 0.0:
            truncated = True

        self.world.update(
            self.current_state,
            self.current_action,
            self.current_reward,
            terminated,
            self.current_energy
        )

        self.render()
        time.sleep(self.delay)
        return self.current_state, self.current_reward, terminated, truncated, {}

    def render(self):
        self.world.render()

    def close(self):
        self.world.close()
