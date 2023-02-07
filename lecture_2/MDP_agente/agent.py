import numpy as np
import pprint


class MDPAgent():
    def __init__(self, states_n, actions_n, P, gamma):
        self.states_n = states_n
        self.actions_n = actions_n
        self.P = P
        self.gamma = gamma
        self.optimal_policy_found = True
        self.reset()

    def reset(self):
        self.values = np.zeros(self.states_n)
        self.policy = np.zeros(self.states_n)

    def get_action(self, state):
        return int(self.policy[state])

    def render(self):
        pprint.pprint(self.values)
        pprint.pprint(self.policy)

    def solve(self, iterations, mode='value-iteration'):
        if(mode == 'value-iteration'):
            self.value_teration(iterations)
        elif(mode == 'policy-iteration'):
            self.policy_iteration(iterations)

    def value_teration(self, iterations):
        for _ in range(iterations):
            for s in range(self.states_n):
                values = [sum([prob * (r + self.gamma * self.values[s_])
                               for prob, s_, r, _ in self.P[s][a]])
                          for a in range(self.actions_n)]
                self.values[s] = max(values)
                self.policy[s] = np.argmax(np.array(values))

    def policy_iteration(self, iterations):
        # Policy evaluation
        def policy_evaluation():
            for i in range(iterations):
                for s in range(self.states_n):
                    values = [sum([prob * (r + self.gamma * self.values[s_next])
                                for prob, s_next, r, _ in self.P[s][self.policy[s]]])]
                    self.values[s] = max(values)

                policy_improvement()
                if self.optimal_policy_found:
                    break

        def policy_improvement():
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


        # Compute value for each state under current policy
        policy_evaluation()
