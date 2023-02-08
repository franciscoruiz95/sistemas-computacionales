import os
import gym
from agent import MDPAgent

# Allowing environment to have sounds
if "SDL_AUDIODRIVER" in os.environ:
    del os.environ["SDL_AUDIODRIVER"]

# RobotBattery-v0, FrozenLake-v1, FrozenLake-v2
env = gym.make('FrozenLake-v1', render_mode=None, is_slippery=True)

gamma_array = [round(value*0.1, 2) for value in range(1, 11)]

iterations = 10000

experiments_number = 2000

for gamma in gamma_array:
    agent = MDPAgent(env.observation_space.n, env.action_space.n, env.P, gamma, iterations)
    mode = agent.solve("value-iteration")
    print("----------------------------------------------------------------------------")
    print(f"Solving with MODE = {mode}({iterations}) | GAMMA = {gamma} | EXPERIMENTS = {experiments_number}")
    agent.render()
    total_reward = [0]
    for _ in range(experiments_number):

        reward_per_run = 0
        observation, info = env.reset()
        terminated, truncated = False, False

        while not (terminated or truncated):
            action = agent.get_action(observation)
            observation, reward, terminated, truncated, _ = env.step(action)
            reward_per_run += reward
        env.close()
        total_reward.append(reward_per_run)

    t = sum(total_reward)
    print(f"Total reward after {experiments_number} experiments is: {t}")
    print(f"Success rate: {round((t / experiments_number) * 100, 2)}%")
    print("---------------------------------------------------------------------------- \n")


