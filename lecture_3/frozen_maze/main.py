import gym
import time
import gym_environments
import numpy as np
from agent import MonteCarlo
from deterministic_agent import MonteCarloAgent as MonteCarloExploringStarts
from frozen_maze_evn.frozen_maze import FrozenMazeEnv


def train_monte_carlo_exploring_starts(env, agent, episodes):
    for _ in range(episodes):
        state, _ = env.reset()
        episode_data = []

        terminated, truncated = False, False
        while not (terminated or truncated):
            action = agent.get_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            episode_data.append((state, action, reward))
            state = next_state

        agent.update(episode_data)


def play_monte_carlo_exploring_starts(env, agent, runs):
    total_reward = 0
    for _ in range(runs):
        state, _ = env.reset()
        terminated, truncated = False, False
        while not (terminated or truncated):
            action = np.argmax(agent.Q[state])
            state, reward, terminated, truncated, _ = env.step(action)
            # env.render()
            # time.sleep(0.1)
            total_reward += reward
    return total_reward


def train_monte_carlo(env, agent, episodes):
    for _ in range(episodes):
        episode = []
        observation, _ = env.reset()
        terminated = False
        while not terminated:
            action = agent.get_action(observation)
            new_observation, reward, terminated, _, _ = env.step(action)
            episode.append((observation, action, reward))
            observation = new_observation
        agent.update(episode)


def play_monte_carlo(env, agent, runs):
    total_reward = 0
    for _ in range(runs):
        observation, _ = env.reset()
        terminated = False
        while not terminated:
            action = agent.get_best_action(observation)
            observation, reward, terminated, _, _ = env.step(action)
            total_reward += reward
            # env.render()
            # time.sleep(0.01)
    return total_reward


if __name__ == "__main__":
    env = gym.make("FrozenMaze-v0", render_mode=None)

    result_monte_carlo = []

    result_exploring_starts = []

    # for epsilon in e_array:
    print("\n----------------------------------------------------")
    print('Gamma: ', 0.9, 'Epsilon: ', 0.3)
    print("----------------------------------------------------\n")
    agent_monte_carlo = MonteCarlo(env.observation_space.n,
                                   env.action_space.n, gamma=0.9, epsilon=0.3)

    agent_exploring_starts = MonteCarloExploringStarts(env.observation_space,
                                                       env.action_space, gamma=0.9, epsilon=0.3)

    train_monte_carlo(env, agent_monte_carlo, episodes=5000)

    agent_monte_carlo.render()
    agent_monte_carlo.print_policy()

    train_monte_carlo_exploring_starts(
        env, agent_exploring_starts, episodes=5000)

    agent_exploring_starts.render()
    agent_exploring_starts.print_policy()

    for _ in range(100):
        result_monte_carlo.append(
            play_monte_carlo(env, agent_monte_carlo, 100))

    for _ in range(100):
        result_exploring_starts.append(
            play_monte_carlo_exploring_starts(env, agent_exploring_starts, 100))

    # for _ in range(100):

    print(
        f"\nTotal average reward monte carlo: {sum(result_monte_carlo) / len(result_monte_carlo)}\n")

    print(
        f"\nTotal average reward exploring starts: {sum(result_exploring_starts) / len(result_exploring_starts)}\n")

    env.close()
