import numpy as np
import sys
import time
import gym
import gym_environments
import matplotlib
import matplotlib.pyplot as plt
from snake.SnakeGym import SnakeGym
from snake.agent import DoubleQLearning


def train(env, agent, episodes):
    for episode in range(episodes):
        if episode % 100 == 0:
            print(f'Episode {episode} \nTrainig...')
        observation, _ = env.reset()
        terminated, truncated = False, False
        while not (terminated or truncated):

            action = agent.get_action(observation, "epsilon-greedy")
            new_observation, reward, terminated, truncated, _ = env.step(
                action)
            # print(new_observation, reward, terminated, truncated, _)
            env.render()
            agent.update(observation, action, new_observation,
                         reward, terminated or truncated)
            observation = new_observation


def play(env, agent):
    observation, _ = env.reset()
    terminated, truncated = False, False

    env.render()
    time.sleep(0.1)

    while not (terminated or truncated):
        action = agent.get_action(observation, "greedy")
        new_observation, reward, terminated, truncated, _ = env.step(action)
        agent.update(observation, action, new_observation,
                     reward, terminated or truncated)
        observation = new_observation


def graph(agent1, agent2, environment, episodes, action):
    if action == 'train':
        x_agent1 = np.linspace(0, agent1.episode, agent1.episode)
        x_agent2 = np.linspace(0, agent2.episode, agent2.episode)

        plt.plot(x_agent1, agent1.reward_for_episode,
                 label='Rewards Q-learning')
        plt.plot(x_agent2, agent2.reward_for_episode,
                 label='Rewards D_Q-learning')

        plt.xlabel('Episodes')
        plt.ylabel('Reward')
        plt.title(f"Q-Learning vs. Double Q-Learning on {environment}")
        plt.legend()
        plt.savefig(
            f'pic/{episodes}-{environment}-Q-Learning-vs-DoubleQ-Learning.png')

    elif action == 'play':
        x = np.linspace(1, 1, 1)
        y1_reward = np.linspace(
            0, agent1.reward_total_finish, abs(agent1.reward_total_finish))
        y2_reward = np.linspace(
            0, agent2.reward_total_finish, abs(agent2.reward_total_finish))
        width = 0.25

        fig, ax = plt.subplots()

        ax.bar(x - width/2, y1_reward, width, label='Q-Learning ')
        ax.bar(x + width/2, y2_reward, width, label='Double Q-Learning')

        ax.set_ylabel('Total Reward')
        ax.set_title(
            f'Q-Learning vs. Double Q-Learning on {environment}\n Play with {episodes} Training episodes')
        ax.set_xticks(x)
        ax.set_xticklabels(x)
        ax.legend()

        fig.tight_layout()
        plt.savefig(
            f'pic/Play-with-Train-{episodes}-{environment}-QL-vs-DQL.png')


if __name__ == "__main__":

    episodes = 1000

    agent = DoubleQLearning(
        18*18, 4, alpha=0.1, gamma=0.9, epsilon=0.5
    )

    env = gym.make("CustomSnake-v0")

    env.reset()

    env.render()

    env.close()

    # play(env, agent1)
    # env.close()
