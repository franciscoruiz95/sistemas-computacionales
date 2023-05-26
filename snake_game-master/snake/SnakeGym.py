import gym

from gym import spaces

import numpy as np

from snake.game import Game

import tkinter as tk

root = tk.Tk()


class SnakeGym(gym.Env):
    metadata = {"render_modes": ["human", "None"], "render_fps": 4}

    def __init__(self):
        '''Set the action and observation spaces
        Initialise the pygame object'''
        super().__init__()
        self.observation_space = spaces.Discrete(18*18)
        self.action_space = spaces.Discrete(4)
        self.current_action = 1
        self.current_state = 0
        self.current_reward = 0
        self.snake = Game(root)


    def reset(self, seed=None, options=None):
        ''' Retorna el estado inicial '''
        super().reset(seed=seed)
        # np.random.seed(seed)
        return self.snake.snakeApp.reset(None), {}

    def get_action(self):
        '''helper function to return keyboard inputs'''
        return self.pygame.get_human_action()

    def step(self, action):
        '''Take action & update the env
        Return -> next-state, reward, done, info'''
        observation, reward, terminated = self.snake.snakeApp.apply_action(action)
        return observation, reward, terminated, False, {}

    def render(self):
        '''Render the env on the screen'''
        self.snake.main_loop()

    def play(self, max_try):
        '''Simulate 1 episode of Single player game'''
        score = 0
        self.reset()
        for t in range(max_try):
            reward, done = self.pygame.run_game_loop()
            score += reward
            if done:
                break
        self.reset()
        return score, done, {'time': t}

    def close(self):
        '''close the pygame object and window'''
        self.snake.quit_game()
