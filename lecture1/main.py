import sys
import gym_environments
import gym
from agent import TwoArmedBandit

num_iterations = 100 if len(sys.argv) < 2 else int(sys.argv[1])
version = "v0" if len(sys.argv) < 3 else sys.argv[2]

num_experiment = 1
alpha = 0.1

env = gym.make(f"TwoArmedBandit-{version}")
agent = TwoArmedBandit(alpha) 

env.reset(options={'delay': 1})

modeArray = ['random', 'greedy', 'epsilon-greedy']
epsilonArray = [0.25, 0.15, 0.1, 0.01]
totalRewardForMode = {}
totalRewardForEpsilon = {}
experimentsDic = {}

for experiment in range(num_experiment):
    for epsilon in epsilonArray: 
        for mode in modeArray:
            print(f'Mode: {mode}')
            for iteration in range(num_iterations):
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

print(f'Results for experimets = {num_experiment} with iterations = {num_iterations} and alpha = {alpha}')
print('----------------------------------------------------')
for epsilon in epsilonArray:
    print(f'Reward average for epsilon = {epsilon}')
    for mode in modeArray:
        tb_or_wsp = 2*'\t' if mode == 'random' or mode == 'greedy' else '\t'
        print(f'in {mode}-mode :{tb_or_wsp}{totalRewardForModeDic[epsilon][mode]/num_experiment}')
    print('----------------------------------------------------')

env.close()