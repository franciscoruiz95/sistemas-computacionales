import sys
import gym_environments
import gym
from agent import TwoArmedBandit

num_iterations = 100 if len(sys.argv) < 2 else int(sys.argv[1])
version = "v0" if len(sys.argv) < 3 else sys.argv[2]

num_experiment = 100

env = gym.make(f"TwoArmedBandit-{version}")
agent = TwoArmedBandit(0.1) 

env.reset(options={'delay': 1})

modeArray = ['random', 'epsilon-greedy']
epsilonArray = [0.5, 0.25, 0.15, 0.1]
totalRewardForMode = {}
totalRewardForEpsilon = {}
experimentsDic = {}

for experiment in range(num_experiment):
    for epsilon in epsilonArray: 
        for mode in modeArray:
            print(f'Mode: ${mode}')
            for _ in range(num_iterations):
                action = agent.get_action(mode, epsilon)
                _, reward, _, _, _ = env.step(action)
                agent.update(action, reward)
                agent.render()
            print('\n')
            agent.print_total_reward()
            agent.get_total_actions()
            print('----------------------------------------------------')
            print('\n')
            totalRewardForMode[mode] = agent.get_total_reward()
            agent.reset()
            
        totalRewardForEpsilon[epsilon] = totalRewardForMode
        totalRewardForMode = {}
    experimentsDic[experiment] = totalRewardForEpsilon
    totalRewardForEpsilon = {}

totalRewardForModeDic = {epsilon : {mode : 0 for mode in modeArray} for epsilon in epsilonArray}

for experiment in range(num_experiment):
    print('++++++++++++++++++++++++++++++++++++++++++')
    print(f'Num Experiment {experiment+1}')
    print('++++++++++++++++++++++++++++++++++++++++++')
    for epsilon in epsilonArray:
        print(f'For epsilon = {epsilon}')
        for mode in modeArray:
            print(f'Mode: {mode} ----- Reward: {experimentsDic[experiment][epsilon][mode]}')
            totalRewardForModeDic[epsilon][mode] +=  experimentsDic[experiment][epsilon][mode]
    
        print('----------------------------------------------------')
    print('***********************************\n')

for epsilon in epsilonArray:
    for mode in modeArray:
        print(f'Average for epsilon = {epsilon} in mode-{mode} : \t{totalRewardForModeDic[epsilon][mode]/num_experiment}')
env.close()