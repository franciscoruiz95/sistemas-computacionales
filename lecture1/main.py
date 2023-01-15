import sys
import gym_environments
import gym
from agent import TwoArmedBandit

num_iterations = 100 if len(sys.argv) < 2 else int(sys.argv[1])
version = "v0" if len(sys.argv) < 3 else sys.argv[2]

env = gym.make(f"TwoArmedBandit-{version}")
agent = TwoArmedBandit(0.1) 

env.reset(options={'delay': 1})

modeArray = ['random', 'epsilon-greedy']
totalRewardArray = {}

for mode in modeArray:
    print(f'Mode: ${mode}')
    for _ in range(num_iterations):
        action = agent.get_action(mode, .15)
        _, reward, _, _, _ = env.step(action)
        agent.update(action, reward)
        agent.render()
    print('\n')
    agent.print_total_reward()
    agent.get_total_actions()
    print('----------------------------------------------------')
    print('\n')
    totalRewardArray[mode] = agent.get_total_reward()
    agent.reset()

for mode in modeArray:
    print(f'Mode: {mode} ----- Reward: {totalRewardArray[mode]}')
env.close()