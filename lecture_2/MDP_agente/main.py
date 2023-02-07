import os

import gym
import gym_environments
from agent import MDPAgent
import time

# Allowing environment to have sounds
if "SDL_AUDIODRIVER" in os.environ:
    del os.environ["SDL_AUDIODRIVER"]

# RobotBattery-v0, FrozenLake-v1, FrozenLake-v2
env = gym.make('FrozenLake-v1', render_mode="human", is_slippery=True)

agent1 = MDPAgent(env.observation_space.n, env.action_space.n, env.P)
agent2 = MDPAgent(env.observation_space.n, env.action_space.n, env.P)

gamma_array = [round(value*0.1, 2) for value in range(10)]

for gamma in gamma_array:
    agent1.set_gamma(gamma)
    agent1.solve(10000, mode='value-iteration')
    agent1.render()
    agent1.reset()

for gamma in gamma_array:
    agent2.set_gamma(gamma)
    agent2.solve(10000, mode='policy-iteration')
    agent2.render()
    agent2.reset()
    

observation, info = env.reset()
terminated, truncated = False, False

env.render()
time.sleep(2)

while not (terminated or truncated):
    action = agent.get_action(observation)
    observation, _, terminated, truncated, _ = env.step(action)

time.sleep(2)
env.close()
