"""
ISPTSC 2023
Lecture 1

Author: Alejandro Mujica - alejandro.j.mujic4@gmail.com
Author: Jesús Pérez - perezj89@gmail.com

This file contains the Agent that plays on the Two-Armed Bandit
Environment.
"""
import numpy as np


class TwoArmedBanditAgent():
    def __init__(self, alpha=1, num_arms=2, seed=None):
        self.alpha = alpha
        self.num_arms = num_arms
        self.action = None
        self.reward = None
        self.iteration = None
        self.values = None
        self.reset(seed)

    def reset(self, seed=None):
        self.action = 0
        self.reward = 0
        self.iteration = 0
        self.values = np.zeros(self.num_arms)
        np.random.seed(seed)

    def update(self, action, reward):
        self.action = action
        self.reward = reward
        self.iteration += 1
        self.values[action] = self.values[action] + self.alpha * (reward - self.values[action])

    def get_action(self, mode):
        if mode == 'random':
            return np.random.choice(self.num_arms)
        elif mode == 'greedy':
            return np.argmax(self.values)

    def render(self):
        print("Iteration: {}, Action: {}, Reward: {}, Values: {}".format(
            self.iteration, self.action, self.reward, self.values))
