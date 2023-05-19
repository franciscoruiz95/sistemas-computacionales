import gym
import time
import gym_environments
from agent import MonteCarlo
from frozen_maze_evn.frozen_maze import FrozenMazeEnv


def train(env, agent, episodes):
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


def play(env, agent):
    observation, _ = env.reset()
    terminated = False
    while not terminated:
        action = agent.get_best_action(observation)
        observation, reward, terminated, _, _ = env.step(action)
        env.render()
        time.sleep(0.1)
    return reward


if __name__ == "__main__":
    env = gym.make("FrozenMaze-v0", is_slippery=False)
    agent = MonteCarlo(env.observation_space.n,
                       env.action_space.n, gamma=0.9, epsilon=0.3)

    train(env, agent, episodes=1000)

    agent.render()

    result = play(env, agent)

    print(f"Total reward: {result}")

    env.close()
