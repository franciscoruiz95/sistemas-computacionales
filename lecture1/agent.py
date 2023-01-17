import numpy as np

class TwoArmedBandit():
    def __init__(self, alpha=1):
        self.arms           = 2
        self.alpha          = alpha
        self.reset()

    def reset(self):
        self.action = 0
        self.reward = 0
        self.iteration = 0
        self.total_reward = 0
        self.total_actions = np.zeros(self.arms)
        self.values = np.zeros(self.arms)
        #self.values = np.random.rand(self.arms)

    def update(self, action, reward):
        self.action = action
        self.reward = reward
        self.iteration += 1
        self.values[action] = self.values[action] + self.alpha * (reward - self.values[action])
        self.total_reward += reward

    def get_action(self, mode, epsilon=0.1):
        if mode == 'random':
            return np.random.choice(self.arms)
        elif mode == 'greedy':
            return np.argmax(self.values)
        elif mode == 'epsilon-greedy':
            pr =  np.random.random()  # [0.0, 1.0)
            action = np.random.choice(self.arms) if pr < epsilon else np.argmax(self.values)

            self.total_actions[action] += 1
            return  action 
                
    def render(self):
        print("Iteration: {}, Action: {}, Reward: {}, Values: {}".format(
            self.iteration, self.action, self.reward, self.values))
    
    def print_total_reward(self):
        print(f"Total reward: {self.total_reward}")
    
    def get_total_reward(self):
        return self.total_reward

    def print_total_actions(self):
        print(f"Total action 0: {self.total_actions[0]} ----- Total action 1: {self.total_actions[1]}")
    
    def get_total_actions(self):
        return self.total_actions