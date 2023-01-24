"""
ISPTSC 2023
Lecture 1

Author: Alejandro Mujica - alejandro.j.mujic4@gmail.com
Author: Jesús Pérez - perezj89@gmail.com

Author: José Briceño - bricenoj9@gmail.com
Author: Francisco Peña - javierrupe19@gmail.com
This file contains the main script to run the Two-Armed Bandit Environment.
"""
import sys

import gym

import environment
from agent import TwoArmedBanditAgent

def main(num_iterations):
    env = gym.make("TwoArmedBanditEnv-v2")
    agent = TwoArmedBanditAgent(0.1, env.action_space.n)

    env.reset(seed=30)

    for _ in range(num_iterations):
        action = agent.get_action("random")
        _, reward, _, _, _ = env.step(action)
        agent.update(action, reward)
        agent.render()
    print(f"Total reeard: {agent.get_total_reward()}")

    env.close()

if __name__ == "__main__":
    num_iterations = 100 if len(sys.argv) < 2 else int(sys.argv[1])
    main(num_iterations)
