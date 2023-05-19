import gym
import time
import numpy as np


class MonteCarlo:
    def __init__(self, observation_space, action_space, gamma=1.0, epsilon=0.1):
        self.observation_space = observation_space
        self.action_space = action_space
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = np.zeros((observation_space, action_space))
        self.N = np.zeros((observation_space, action_space))

    def get_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.action_space)
        else:
            return np.argmax(self.Q[state])

    def update(self, episode):
        states, actions, rewards = zip(*episode)
        discounts = np.array([self.gamma**i for i in range(len(rewards))])
        returns = np.cumsum(rewards[::-1] * discounts[::-1])[::-1]
        for i, state in enumerate(states):
            action = actions[i]
            self.N[state][action] += 1
            alpha = 1 / self.N[state][action]  # Step size
            self.Q[state][action] += alpha * \
                (returns[i] - self.Q[state][action])

    def get_best_action(self, state):
        return np.argmax(self.Q[state])

    def render(self):
        print("Q-Values:")
        print(self.Q)
