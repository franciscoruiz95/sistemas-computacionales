import numpy as np
import pprint
from .KruskalsMazeGenerator import KruskalsMazeGenerate as KMaze

#Generate random P matrix
class PMatrix:
    def __init__(self, width=4, height=4, actions=4):
        self.actions = actions
        self.width = width
        self.height = height
        self.states = width * height
        self.maze = KMaze(width, height)
        self.holes = self.__generate_random_holes()

        # P matrix
        self.P = {
                    s : {
                            a : [] for a in range(self.actions)
                        } for s in range(self.states) 
                }
        self.__create_p_matrix()

    def __create_p_matrix(self):

        for i in range(self.height):
            for j in range(self.width):

                left    = 0 if j == 0 else j - 1
                down    = self.height - 1 if i == self.height - 1 else i + 1
                right   = self.width - 1 if j == self.width - 1 else j + 1
                up      = 0 if i == 0 else i - 1

                state   = i * self.width + j

                if self.__is_terminal(state):
                    self.P[state] = {
                        a : [(1.0, state, 0, True)] for a in range(self.actions)
                    }
                else:
                    probability = 1.0 / 3.0
                    left_state  = state if self.maze.walls[state]['W'] else i * self.width + left 
                    down_state  = state if self.maze.walls[state]['S'] else down * self.width + j
                    right_state = state if self.maze.walls[state]['E'] else i * self.width + right
                    up_state    = state if self.maze.walls[state]['N'] else up * self.width + j

                    # The action Left will change to the left, down, or up with the same probability
                    self.P[state][0] = [
                        (probability, left_state, self.__reward(left_state), self.__is_terminal(left_state)),
                        (probability, down_state, self.__reward(down_state), self.__is_terminal(down_state)),
                        (probability, up_state, self.__reward(up_state), self.__is_terminal(up_state)),
                    ]
                    
                    # The action Down will change to the down, left, or right with the same probability
                    self.P[state][1] = [
                        (probability, down_state, self.__reward(down_state), self.__is_terminal(down_state)),
                        (probability, left_state, self.__reward(left_state), self.__is_terminal(left_state)),
                        (probability, right_state, self.__reward(right_state), self.__is_terminal(right_state)),
                    ]

                    # The action Right will change to the right, up, or down with the same probability

                    self.P[state][2] = [
                        (probability, right_state, self.__reward(right_state), self.__is_terminal(right_state)),
                        (probability, up_state, self.__reward(up_state), self.__is_terminal(up_state)),
                        (probability, down_state, self.__reward(down_state), self.__is_terminal(down_state)),
                    ]
                
                    # The action Up will change to the up, left, or right with the same probability
                    self.P[state][3] = [
                        (probability, up_state, self.__reward(up_state), self.__is_terminal(up_state)),
                        (probability, left_state, self.__reward(left_state), self.__is_terminal(left_state)),
                        (probability, right_state, self.__reward(right_state), self.__is_terminal(right_state)),
                    ]

        return

    def __reward(self, state_):
        return 1 \
            if state_ == state_ == self.states-1 \
            else 0

    def __is_terminal(self, state_):
        return True \
            if state_ == self.states-1 or state_ in self.holes \
            else False
    
    def __generate_random_holes(self):
        # Random states list size
        n_holes = int(self.states * 0.15)

        # List to save random states that are not on path
        random_holes = []

        # Generate random points until you have n_holes that are not in path
        while len(random_holes) < n_holes:
            # Generate a random state
            random_hole = np.random.choice(range(1, self.states-1), replace=False)
            # Check if random states is not in path
            if random_hole not in self.maze.path:
                random_holes.append(random_hole)

        return random_holes
    

# p = PMatrix(width=2, height=2, actions=4)

# pprint.pprint(p.maze.path)
# pprint.pprint(p.holes)
# pprint.pprint(p.P)


