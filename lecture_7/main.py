import sys
import gym
import gym_environments
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from agent import DYNAQ
from agent2 import DYNAQPlus


def run(env, agent: DYNAQ, selection_method, episodes):
    for episode in range(1, episodes+1):
        if episode % 10 == 0:
            print(f"Episode: {episode}")
        observation, _ = env.reset()
        agent.start_episode()
        terminated, truncated = False, False
        while not (terminated or truncated):
            action = agent.get_action(observation, selection_method)
            next_observation, reward, terminated, truncated, _ = env.step(action)
            agent.update_q(observation, action, next_observation, reward)
            agent.update_model(observation, action, reward, next_observation)
            observation = next_observation
        if selection_method == "epsilon-greedy":
            for _ in range(100):
                state = np.random.choice(list(agent.visited_states.keys()))
                action = np.random.choice(agent.visited_states[state])
                reward, next_state = agent.model[(state, action)]
                agent.update_q(state, action, next_state, reward)

            agent.update_steps_for_episode()

def graph(agent1, agent2, environment, episodes_train, episodes_play, action):
    if action == 'train':
        x_agent1 = np.linspace(1, agent1.episode, episodes_train)
        x_agent2 = np.linspace(1, agent2.episode, episodes_train)

        plt.plot(x_agent1, agent1.get_steps_for_episodes(), label='DYNAQ')
        plt.plot(x_agent2, agent2.get_steps_for_episodes(), label='DYNAQPlus')
        
        plt.xlabel('Episodes')
        plt.ylabel('Steps for Episode')
        plt.title(f"DYNA-Q vs. DYNA-Q Plus on {environment}")
        plt.legend()
        plt.savefig(f'pic/{episodes}-{environment}-DYNAQ-vs-DYNAQPlus.png')
    
    elif action == 'play':
        x = np.linspace(1, episodes_play, episodes_play)
        y1_steps = np.linspace(0, agent1.step, agent1.step)
        y2_steps = np.linspace(0, agent2.step, agent2.step)
        width = 0.25

        fig, ax = plt.subplots()

        ax.bar(x - width/2, y1_steps, width, label='DYNAQ')
        ax.bar(x + width/2, y2_steps, width, label='DYNAQPlus')

        ax.set_ylabel('Steps for Episode')
        ax.set_title(f'DYNA-Q vs. DYNA-Q Plus on {environment}\n Play with {episodes_train} Training episodes')
        ax.set_xticks(x)
        ax.set_xticklabels(x)
        ax.legend()

        fig.tight_layout()
        plt.savefig(f'pic/Play-{episodes_play}-Train-{episodes_train}-{environment}-DQ-vs-DQPlus.png')




if __name__ == "__main__":
    environments = ["Princess-v0", "Blocks-v0"]
    id = 0 if len(sys.argv) < 2 else int(sys.argv[1])
    episodes = 350 if len(sys.argv) < 3 else int(sys.argv[2])
    env = gym.make(environments[id])
    agent1 = DYNAQ(env.observation_space.n, env.action_space.n, alpha=1, gamma=0.95, epsilon=0.1)
    agent2 = DYNAQPlus(env.observation_space.n, env.action_space.n, alpha=1, gamma=0.95, epsilon=0.1, kappa=0.1)

    # Train for agent1
    print("Agent: DYNA-Q")
    run(env, agent1, "epsilon-greedy", episodes)

    print("*************************************")

    # Train for agent2
    print("Agent: DYNA-Q Plus")
    run(env, agent2, "epsilon-greedy", episodes)

    print("*************************************")

    env.close()
    
    #graphs
    graph(agent1, agent2, environments[id], episodes, 1, 'train')

    # Play for agent1
    env = gym.make(environments[id], render_mode="human")
    run(env, agent1, "greedy", 1)
    agent1.render()
    env.close()

    # Play for agent1
    env = gym.make(environments[id], render_mode="human")
    run(env, agent2, "greedy", 1)
    agent2.render()
    env.close()

    graph(agent1, agent2, environments[id], episodes, 1, 'play')

