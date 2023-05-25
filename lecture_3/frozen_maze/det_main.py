import gym
import time
import numpy as np
import gym_environments
from deterministic_agent import MonteCarloAgent
from frozen_maze_evn.frozen_maze import FrozenMazeEnv


def train(env, agent, episodes):
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


def play(env, agent, runs):
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


if __name__ == "__main__":
    env = gym.make("FrozenMaze-v0")

    result = []

    # for epsilon in e_array:
    print('\nGamma: ', 0.9, 'Epsilon: ', 0.3)

    agent = MonteCarloAgent(env.observation_space,
                            env.action_space, gamma=0.9, epsilon=0.3)

    train(env, agent, episodes=2000)

    agent.render()

    for _ in range(1000):
        result.append(play(env, agent, 500))

    print(f"\nTotal average reward: {sum(result) / len(result)}\n")

    agent.print_policy()

    # play(env, agent)

    env.close()
