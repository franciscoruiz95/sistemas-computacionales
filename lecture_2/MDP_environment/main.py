import os

import gym
import gym_environments
import time
import robot_battery_env
from agent import MDPAgent

# Allowing environment to have sounds
if "SDL_AUDIODRIVER" in os.environ:
    del os.environ["SDL_AUDIODRIVER"]

# RobotBattery-v0, 'RobotBattery-v1', FrozenLake-v1, FrozenLake-v2
env = gym.make('RobotBattery-v1', render_mode="human")
iterations = 10000
agent = MDPAgent(env.observation_space.n, env.action_space.n, env.P, 0.9, iterations)
mode = agent.solve("value-iteration")

agent.solve(1000)
agent.render()

observation, info = env.reset()
terminated, truncated = False, False

env.render()
time.sleep(2)

while not ((terminated) or truncated):
    action = agent.get_action(observation)
    observation, _, terminated, truncated, _ = env.step(action)

time.sleep(5)
env.close()
