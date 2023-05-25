import numpy as np
import random
import gym


class MonteCarloAgent:
    def __init__(self, observation_space, action_space, gamma=0.9, epsilon=0.1):
        self.observation_space = observation_space
        self.action_space = action_space
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = np.zeros((observation_space.n, action_space.n))
        self.N = np.zeros((observation_space.n, action_space.n), dtype=int)
        self.pi = np.zeros(observation_space.n, dtype=int)

    def get_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            action = self.action_space.sample()  # Explore
        else:
            action = np.argmax(self.Q[state])  # Exploit
        return action

    def get_best_action(self, state):
        return np.argmax(self.Q[state])

    def print_policy(self):
        optimal_policy = np.argmax(self.Q, axis=1)
        print("\nOptimal Policy for MonteCarlo Exploring Starts:\n")
        print(optimal_policy.reshape((5, 5)))

    def update(self, episode):
        G = 0
        visited_states = set()

        for t in reversed(range(len(episode))):
            state, action, reward = episode[t]
            G = self.gamma * G + reward
            if (state, action) not in visited_states:
                self.N[state, action] += 1
                alpha = 1 / self.N[state, action]
                self.Q[state, action] += alpha * (G - self.Q[state, action])
                visited_states.add((state, action))

    def render(self):
        print(f"\nMonteCarlo Exploring Starts Q-Values:\n\n {self.Q} \n")
