import pprint

# P = {   
#         0: {0: [(1, 0, 0.0, False)], 1: [(1, 2, 0.0, False)], 2: [(1, 1, 0.0, False)], 3: [(1, 0, 0.0, False)]},
#         1: {0: [(1, 0, 0.0, False)], 1: [(1, 3, 0.0, False)], 2: [(1, 1, 0.0, False)], 3: [(1, 1, 0.0, False)]},
#         2: {0: [(1, 2, 0.0, False)], 1: [(1, 4, 0.0, False)], 2: [(1, 3, 0.0, False)], 3: [(1, 0, 0.0, False)]},
#         3: {0: [(1, 2, 0.0, False)], 1: [(1, 5, 1.0, True)], 2: [(1, 3, 0.0, False)], 3: [(1, 1, 0.0, False)]},
#         4: {0: [(1, 4, 0.0, False)], 1: [(1, 4, 0.0, False)], 2: [(1, 5, 1.0, True)], 3: [(1, 2, 0.0, False)]},
#         5: {0: [(1, 5, 0.0, True)], 1: [(1, 5, 0.0, True)], 2: [(1, 5, 0.0, True)], 3: [(1, 5, 0.0, True)]}
#     }

ACTION = 4
N = 16
STATES = pow(N, 2)

def next_state(current_state, action):
    row = current_state // N
    col = current_state % N

    if (current_state == 0 and action in [0 , 3]) or \
            (current_state == N-1 and action == 2) or \
                    (row == 0 and action == 3)      or \
                        (current_state == STATES-1)  or \
                            (row == N-1 and action == 1) or\
                                (current_state == STATES-N and action in [0, 1]) or\
                                    (col == 0 and action == 0) or \
                                        (col == N-1 and action == 2):
        return current_state

    if (row > 0 and row <= N-1 and action == 0):
        return current_state - 1

    if (row >= 0 and row <= N-2 and action == 1):
        return current_state + N

    if (row >= 0 and row <= N-1 and action == 2):
        return current_state + 1

    if (row > 0 and row <= N-1 and action == 3):
        return current_state - N


def reward(current_state, action):
    return 1.0 \
        if (current_state == STATES-N-1 and action == 1) or \
            (current_state == STATES-2 and action == 2) \
        else 0.0

def is_terminal(current_state, action):
    return True\
        if (current_state == STATES-N-1 and action == 1) or \
                (current_state == STATES-2 and action == 2) or\
                    (current_state == STATES-1)\
        else False

P = {
            s : {
                a : [(
                    1, next_state(s, a), reward(s, a), is_terminal(s, a)
                )] for a in range(ACTION)
            } for s in range(STATES) 
        }

pprint.pprint(P)