import numpy as np
from maze_generator.KruskalsMazeGenerator import KruskalsMazeGenerate as  KMaze


#Generate random P matrix
class PMatrix:
    def __init__(self, width=4, height=4, actions=4, n=16):
        self.actions = actions
        self.n = n
        self.states = pow(n, 2)
        self.maze = KMaze(width, height)
        self.holes = self.__generate_random_holes()

        # P matrix
        self.P = {
                    s : {
                            a : [
                                (0.33, self.__next_state(s, a), self.__reward(s, a), self.__is_terminal(s, a)) 
                            ] for a in range(self.actions)
                        } for s in range(self.states) 
                }

    def __next_state(self, current_state, action):
        row = current_state // self.n
        col = current_state % self.n

        if (current_state == 0 and action in [0 , 3]) or \
                (current_state == self.n-1 and action == 2) or \
                        (row == 0 and action == 3)      or \
                            (current_state == self.states - 1)  or \
                                (row == self.n-1 and action == 1) or\
                                    (current_state == self.states - self.n and action in [0, 1]) or\
                                        (col == 0 and action == 0) or \
                                            (col == self.n - 1 and action == 2):
            return current_state

        if (row >= 0 and row <= self.n - 1 and action == 0):
            return current_state - 1

        if (row >= 0 and row <= self.n - 2 and action == 1):
            return current_state + self.n

        if (row >= 0 and row <= self.n - 1 and action == 2):
            return current_state + 1

        if (row > 0 and row <= self.n - 1 and action == 3):
            return current_state - self.n


    def __reward(self, current_state, action):
        return 1.0 \
            if (current_state == self.states-self.n-1 and action == 1) or \
                (current_state == self.states-2 and action == 2) \
            else 0.0

    def __is_terminal(self, current_state, action):
        return True\
            if (current_state == self.states-self.n-1 and action == 1) or \
                    (current_state == self.states-2 and action == 2) or\
                        (current_state == self.states-1)\
            else False
    
    def __generate_random_holes(self):
        return np.random.choice(range(1, self.n-1), int(self.n * 0.25), replace=False)
    
    # def __path(self):
    #     path = self.__dijkstrac()
    #     return path
    
    # #dijkstrac's algorithm
    # def __dijkstrac():
    #     return