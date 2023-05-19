import numpy as np
import sys
import time
import gym
import gym_environments
import matplotlib
import matplotlib.pyplot as plt
from agent import QLearning
from double_agent import DoubleQLearning


def train(env, agent, episodes):
    for episode in range(episodes):
        if episode % 100 == 0:
            print(f'Episode i: {episode} \nTrainig...')
        observation, _ = env.reset()
        terminated, truncated = False, False
        while not (terminated or truncated):
            action = agent.get_action(observation, "epsilon-greedy")
            new_observation, reward, terminated, truncated, _ = env.step(action)
            agent.update(observation, action, new_observation, reward, terminated or truncated)
            observation = new_observation


def play(env, agent):
    observation, _ = env.reset()
    terminated, truncated = False, False

    env.render()
    time.sleep(2)

    while not (terminated or truncated):
        action = agent.get_action(observation, "greedy")
        new_observation, reward, terminated, truncated, _ = env.step(action)
        agent.update(observation, action, new_observation, reward, terminated or truncated)
        observation = new_observation

def graph(agent1, agent2, environment, episodes):
    x_agent1 = np.linspace(0, agent1.episode, agent1.episode)
    x_agent2 = np.linspace(0, agent2.episode, agent2.episode)

    plt.plot(x_agent1, agent1.reward_for_episode, label='Rewards Q-learning')
    plt.plot(x_agent2, agent2.reward_for_episode, label='Rewards D_Q-learning')
    
    plt.xlabel('Episodes')
    plt.ylabel('Reward')
    plt.title(f"Q-Learning vs. Double Q-Learning on {environment}")
    plt.legend()
    plt.savefig(f'pic/{episodes}-{environment}-Q-Learning-vs-DoubleQ-Learning.png')


    
if __name__ == "__main__":
    environments = ["CliffWalking-v0", "Taxi-v3", "Princess-v0", "Blocks-v0"]
    id = 0 if len(sys.argv) < 2 else int(sys.argv[1])
    episodes = 10000 if len(sys.argv) < 3 else int(sys.argv[2])

    env = gym.make(environments[id])
    agent1 = DoubleQLearning(
        env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.5
    )

    train(env, agent1, episodes)
    agent1.render()
    env.close()

    env = gym.make(environments[id], render_mode="human")
    play(env, agent1)
    env.close()

    env = gym.make(environments[id])
    agent2 = QLearning(
        env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.5
    )

    train(env, agent2, episodes)
    agent2.render()
    env.close()

    env = gym.make(environments[id], render_mode="human")
    play(env, agent2)
    env.close()

    graph(agent1, agent2, environments[id], episodes)