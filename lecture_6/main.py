import numpy as np
import sys
import gym
import gym_environments
import numpy as np
from agent import SARSA
from agent2 import ExpectedSARSA
import pprint
import matplotlib
import matplotlib.pyplot as plt

ALPHA = [a/10 for a in range(1, 11)]

def calculate_states_size(env):
    max = env.observation_space.high
    min = env.observation_space.low
    sizes = (max - min) * np.array([10, 100]) + 1
    return int(sizes[0]) * int(sizes[1])


def calculate_state(env, value):
    min = env.observation_space.low
    values = (value - min) * np.array([10, 100])
    return int(values[1]) * 19 + int(values[0])


def run(env, agent, selection_method, episodes):
    for episode in range(1, episodes + 1):
        if episode % 100 == 0:
            print(f"Episode: {episode}")
        observation, _ = env.reset()
        action = agent.get_action(calculate_state(env, observation), selection_method)
        terminated, truncated = False, False
        while not (terminated or truncated):
            new_observation, reward, terminated, truncated, _ = env.step(action)
            next_action = agent.get_action(
                calculate_state(env, new_observation), selection_method
            )
            agent.update(
                calculate_state(env, observation),
                action,
                calculate_state(env, new_observation),
                next_action,
                reward,
                terminated,
                truncated,
            )
            observation = new_observation
            action = next_action

def graph(agent_name, mean_return, episode):

    x = np.arange(len(ALPHA))
    width = 0.35

    fig, ax = plt.subplots()

    ax.bar(x - width/2, mean_return[agent_name[0].__name__], width, label=agent_name[0].__name__)
    ax.bar(x + width/2, mean_return[agent_name[0].__name__], width, label=agent_name[1].__name__)

    ax.set_ylabel('Average Returns')
    ax.set_title(f'{agent_name[0].__name__} vs. {agent_name[1].__name__}')
    ax.set_xticks(x)
    ax.set_xticklabels(ALPHA)
    ax.legend()

    fig.tight_layout()
    plt.savefig(f'pic/{episode}-{agent_name[0].__name__}_Vs_{agent_name[1].__name__}.png')
    # plt.show()


if __name__ == "__main__":
    episodes = 4000 if len(sys.argv) == 1 else int(sys.argv[1])
    agents = [SARSA, ExpectedSARSA]

    episodes_ = [1000, 2000, 3000, 4000]
    env = gym.make("MountainCar-v0")

    for episode in episodes_:
        meanReturn = {}
        for agt in agents:
            print(f"Agent: {agt.__name__}")
            reward_for_episode = []
            for a in ALPHA:
                print(f"For Alpha {a}")
                agent = agt(
                    calculate_states_size(env),
                    env.action_space.n,
                    alpha=a,
                    gamma=0.9,
                    epsilon=0.1,
                )

                # Train
                run(env, agent, "epsilon-greedy", episode)

                # Calculate the mean of sum of returns for each episode in Alpha
                reward_for_episode.append(np.mean(agent.get_reward_for_episode()))
                meanReturn[type(agent).__name__] = reward_for_episode

        graph(agents, meanReturn, episode)

    env.close()



    # Play
    # env = gym.make("MountainCar-v0", render_mode="human")
    # run(env, agent, "greedy", 1)
    # agent.render()
    # env.close()