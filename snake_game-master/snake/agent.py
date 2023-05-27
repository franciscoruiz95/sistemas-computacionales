import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import json
import random
from dataclasses import dataclass


@dataclass
class GameState:
    distance: tuple
    position: tuple
    surroundings: str
    food: tuple


class QLearning:
    def __init__(self, states_n, actions_n, alpha, gamma, epsilon, display_width, display_height, block_size):
        self.states_n = states_n
        self.actions_n = actions_n
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.total_reward = 0
        self.episode = 0
        self.reward_for_episode = []

        self.display_width = display_width
        self.display_height = display_height
        self.block_size = block_size

        # Learning parameters
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

        # State/Action history
        self.qvalues = self.LoadQvalues()
        self.history = []

        # Action space
        self.actions = {
            0: 'left',
            1: 'right',
            2: 'up',
            3: 'down'
        }

        self.reset()

    def reset(self):
        self.history = []

    def LoadQvalues(self, path="qvalues.json"):
        with open(path, "r") as f:
            qvalues = json.load(f)
        return qvalues

    def SaveQvalues(self, path="qvalues.json"):
        with open(path, "w") as f:
            json.dump(self.qvalues, f)

    def update(self, reason, score):
        if reason:
            self.reward_for_episode.append(score)
            print("Score", score)

        history = self.history[::-1]
        for i, h in enumerate(history[:-1]):
            if reason:  # Snake Died -> Negative reward
                sN = history[0]['state']
                aN = history[0]['action']
                state_str = self._GetStateStr(sN)
                reward = -1
                # Bellman equation - there is no future state since game is over
                self.qvalues[state_str][aN] = (
                    1-self.alpha) * self.qvalues[state_str][aN] + self.alpha * reward
                reason = None
            else:
                s1 = h['state']  # current state
                s0 = history[i+1]['state']  # previous state
                a0 = history[i+1]['action']  # action taken at previous state

                x1 = s0.distance[0]  # x distance at current state
                y1 = s0.distance[1]  # y distance at current state

                x2 = s1.distance[0]  # x distance at previous state
                y2 = s1.distance[1]  # y distance at previous state

                if s0.food != s1.food:  # Snake ate a food, positive reward
                    reward = 1
                # Snake is closer to the food, positive reward
                elif (abs(x1) > abs(x2) or abs(y1) > abs(y2)):
                    reward = 1
                else:
                    reward = -1  # Snake is further from the food, negative reward

                state_str = self._GetStateStr(s0)
                new_state_str = self._GetStateStr(s1)
                self.qvalues[state_str][a0] = (1-self.alpha) * (self.qvalues[state_str][a0]) + self.alpha * (
                    reward + self.gamma*max(self.qvalues[new_state_str]))  # Bellman equation

    def _GetStateStr(self, state):
        return str((state.position[0], state.position[1], state.surroundings))

    def _GetState(self, snake, food):
        snake_head = snake[0]
        dist_x = food[0] - snake_head[0]
        dist_y = food[1] - snake_head[1]

        if dist_x > 0:
            pos_x = '1'  # Food is to the right of the snake
        elif dist_x < 0:
            pos_x = '0'  # Food is to the left of the snake
        else:
            pos_x = 'NA'  # Food and snake are on the same X file

        if dist_y > 0:
            pos_y = '3'  # Food is below snake
        elif dist_y < 0:
            pos_y = '2'  # Food is above snake
        else:
            pos_y = 'NA'  # Food and snake are on the same Y file

        sqs = [
            (snake_head[0]-self.block_size, snake_head[1]),
            (snake_head[0]+self.block_size, snake_head[1]),
            (snake_head[0],                  snake_head[1]-self.block_size),
            (snake_head[0],                  snake_head[1]+self.block_size),
        ]

        surrounding_list = []
        for sq in sqs:
            if sq[0] < 0 or sq[1] < 0:  # off screen left or top
                surrounding_list.append('1')
            # off screen right or bottom
            elif sq[0] >= self.display_width or sq[1] >= self.display_height:
                surrounding_list.append('1')
            elif sq in snake[:-1]:  # part of tail
                surrounding_list.append('1')
            else:
                surrounding_list.append('0')
        surroundings = ''.join(surrounding_list)

        return GameState((dist_x, dist_y), (pos_x, pos_y), surroundings, food)

    def get_action(self, snake, food, mode):
        state = self._GetState(snake, food)
        # Epsilon greedy
        if mode == 'epsilon-greedy':
            rand = random.uniform(0, 1)
            if rand < self.epsilon:
                action_key = np.random.choice(list(self.actions.keys()))
            else:
                state_scores = self.qvalues[self._GetStateStr(state)]
                action_key = state_scores.index(max(state_scores))
            action_val = self.actions[action_key]
        else:
            state_scores = self.qvalues[self._GetStateStr(state)]
            action_key = state_scores.index(max(state_scores))

        # Remember the actions it took at each state
        self.history.append({
            'state': state,
            'action': action_key
        })
        return action_key

    def render(self, mode="values"):
        if mode == "step":
            print(
                "Episode: {}, Iteration: {}, State: {}, Action: {}, Next state: {}, Reward: {}".format(
                    self.episode,
                    self.iteration,
                    self.state,
                    self.action,
                    self.next_state,
                    self.reward,
                )
            )
        elif mode == "values":
            print("Q1: {}\nQ2: {}".format(self.q1, self.q2))
            print(self.episode)
            print(len(self.reward_for_episode), self.reward_for_episode)

    def graph(self):
        x = np.linspace(0, len(self.reward_for_episode), len(self.reward_for_episode))

        plt.plot(x, self.reward_for_episode, label='Q-learning')

        plt.xlabel('Episodes')
        plt.ylabel('Tatal Reward')
        plt.title("Agent learning with Q-Learning\n on Snake ('Epsilon Voráz') Environment")
        plt.legend()
        plt.savefig(f'../resources/graphics/{len(self.reward_for_episode)}-Q-Learning.png')
        # plt.show()
