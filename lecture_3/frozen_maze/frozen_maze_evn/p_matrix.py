import numpy as np

# Define the size of the FrozenLake grid
n = 15

# Define the number of possible actions in the FrozenLake environment
num_actions = 4

# Define the probability of taking the intended action
p_intended = 0.8

# Define the probability of taking a random action
p_random = (1 - p_intended) / (num_actions - 1)

# Create a random P matrix
P = np.zeros((n*n, num_actions, n*n))
for s in range(n*n):
    for a in range(num_actions):
        next_s = s
        # Move up
        if a == 0:
            next_s -= n
        # Move down
        elif a == 1:
            next_s += n
        # Move left
        elif a == 2:
            next_s -= 1
        # Move right
        elif a == 3:
            next_s += 1
        # Check if the next state is a wall or outside the grid
        if next_s < 0 or next_s >= n*n or (s % n == 0 and a == 2) or ((s+1) % n == 0 and a == 3) or (s < n and a == 0) or (s >= n*(n-1) and a == 1):
            next_s = s
        # Set the probability of taking the intended action
        P[s, a, next_s] = p_intended
        # Set the probability of taking a random action
        for other_a in range(num_actions):
            if other_a != a:
                P[s, a, s] += p_random

# Print the P matrix
print(P)
