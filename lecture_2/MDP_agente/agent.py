import numpy as np


class MDPAgent():
    def __init__(self, states_n, actions_n, P, gamma, iterations):
        self.states_n = states_n
        self.actions_n = actions_n
        self.P = P
        self.gamma = gamma
        self.optimal_policy_found = False
        self.iterations = iterations
        self.reset()

    def reset(self):
        self.values = np.zeros(self.states_n)
        self.policy = np.zeros(self.states_n)

    def get_action(self, state):
        return int(self.policy[state])

    def render(self):
        print("----------------------------------------------------------------------------")
        print(f"Values: \n{self.values}")
        print("----------------------------------------------------------------------------")
        print(f"Policy: {self.policy}")
        print("----------------------------------------------------------------------------")

    def solve(self, mode='value-iteration'):
        if(mode == 'value-iteration'):
            self.value_teration()
        elif(mode == 'policy-iteration'):
            self.policy_iteration()
        return mode

    def value_teration(self):
        for t in range(self.iterations):
            for s in range(self.states_n):
                values = [sum([prob * (r + self.gamma * self.values[s_next])
                                for prob, s_next, r, _ in self.P[s][a]])
                            for a in range(self.actions_n)]
                self.values[s] = max(values)
                self.policy[s] = np.argmax(np.array(values))

    def policy_evaluation(self):
        for _ in range(self.iterations):
            for s in range(self.states_n):
                values = [sum([prob * (r + self.gamma * self.values[s_next])
                            for prob, s_next, r, _ in self.P[s][self.policy[s]]])]
                self.values[s] = max(values)

    def policy_improvement(self):
        # Policy improvement
        # With updated state values, improve policy if needed
        self.optimal_policy_found = True

        for s in range(self.states_n):
            old_action = self.policy[s]
            values = [sum([prob * (r + self.gamma * self.values[s_next])
                            for prob, s_next, r, _ in self.P[s][a]])
                        for a in range(self.actions_n)]
            self.policy[s] = np.argmax(np.array(values))

            if old_action != self.policy[s]:
                self.optimal_policy_found = False
    
    def policy_iteration(self):

        while not self.optimal_policy_found:
            self.policy_evaluation()
            self.policy_improvement()
        
