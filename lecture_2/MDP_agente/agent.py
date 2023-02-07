import numpy as np
import pprint


class MDPAgent():
    def __init__(self, states_n, actions_n, P, gamma = 0.0):
        self.states_n = states_n
        self.actions_n = actions_n
        self.P = P
        self.gamma = gamma
        self.resul = True
        self.reset()

    def reset(self):
        self.values = np.zeros(self.states_n)
        self.policy = np.zeros(self.states_n)

    def get_action(self, state):
        return int(self.policy[state])

    def set_gamma(self, gamma):
        self.gamma = gamma

    def render(self):
        print("--------------------------------------------------------------------")
        print(f'Data for gama {self.gamma}')
        print("--------------------------------------------------------------------")
        print(f"Values: {self.values}")
        print("--------------------------------------------------------------------")
        print(f"Policy: {self.policy}")
        print("--------------------------------------------------------------------")
        print("\n")

    def solve(self, iterations, mode='value-iteration'):
        if(mode == 'value-iteration'):
            self.value_iteration(iterations)
        elif(mode == 'policy-iteration'):
            self.policy_iteration(iterations)

    def value_iteration(self, iterations):
        for t in range(iterations):
            for s in range(self.states_n):
                values = [sum([prob * (r + self.gamma * self.values[s_next])
                                for prob, s_next, r, _ in self.P[s][a]])
                            for a in range(self.actions_n)]
                self.values[s] = max(values)
                self.policy[s] = np.argmax(np.array(values))
    
    # Policy evaluation
    def policy_evaluation(self, iterations):
        for i in range(iterations):
            for s in range(self.states_n):
                values = [sum([prob * (r + self.gamma * self.values[s_next])
                            for prob, s_next, r, _ in self.P[s][self.policy[s]]])]
                self.values[s] = max(values)
            self.policy_improvement()
            if self.optimal_policy_found:
                break


    
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

    def policy_iteration(self, iterations):
        # Policy evaluation
        self.policy_evaluation(iterations)

        
