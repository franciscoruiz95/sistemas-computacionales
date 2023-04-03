# import heapq

# # define the maze as a graph
# maze = {
#     (0, 0): [(0, 1)],
#     (0, 1): [(0, 0), (0, 2)],
#     (0, 2): [(0, 1), (0, 3)],
#     (0, 3): [(0, 2), (1, 3)],
#     (1, 3): [(0, 3), (2, 3)],
#     (2, 3): [(1, 3), (3, 3)],
#     (3, 3): [(2, 3), (3, 2)],
#     (3, 2): [(3, 3), (3, 1)],
#     (3, 1): [(3, 2), (3, 0)],
#     (3, 0): [(3, 1), (2, 0)],
#     (2, 0): [(3, 0), (1, 0)],
#     (1, 0): [(2, 0), (0, 0)]
# }

# # define the start and end points
# start = (0, 0)
# end = (3, 0)

# # define a dictionary to store the distances to each point
# distances = {point: float('inf') for point in maze}
# distances[start] = 0

# # define a dictionary to store the previous point in the shortest path
# previous = {point: None for point in maze}

# # define a priority queue to store the points to visit
# queue = [(0, start)]

# # iterate over the priority queue
# while queue:
#     current_distance, current_point = heapq.heappop(queue)

#     # check if the current point is the end point
#     if current_point == end:
#         break

#     # iterate over the neighbors of the current point
#     for neighbor in maze[current_point]:
#         # calculate the distance to the neighbor
#         distance = current_distance + 1

#         # check if the distance to the neighbor is shorter than the current distance
#         if distance < distances[neighbor]:
#             distances[neighbor] = distance
#             previous[neighbor] = current_point
#             heapq.heappush(queue, (distance, neighbor))

# # construct the shortest path
# path = []
# shortest_path = []  # add this line
# current_point = end
# while current_point:
#     path.append(current_point)
#     shortest_path.append(current_point)  # add this line
#     current_point = previous[current_point]
# path.reverse()
# shortest_path.reverse()  # add this line

# # print the shortest path, the distance to the end point, and the shortest path list
# print('Shortest path:', path)
# print('Distance:', distances[end])
# print('Shortest path list:', shortest_path)

import random
import heapq

# define the size of the maze
size = 10

# define a function to generate the maze
def generate_maze(size):
    # create a grid of cells
    grid = [[(row, col) for col in range(size)] for row in range(size)]

    # select the starting cell at random
    current_cell = random.choice(random.choice(grid))

    # create a set to store the visited cells
    visited = {current_cell}

    # create a list to store the edges
    edges = []

    # iterate until all cells have been visited
    while len(visited) < size ** 2:
        # find the neighboring cells that have not been visited
        neighbors = [(row, col) for row, col in [
            (current_cell[0] - 1, current_cell[1]),
            (current_cell[0] + 1, current_cell[1]),
            (current_cell[0], current_cell[1] - 1),
            (current_cell[0], current_cell[1] + 1)
        ] if row >= 0 and row < size and col >= 0 and col < size and (row, col) not in visited]

        # select a random neighboring cell
        if neighbors:
            neighbor = random.choice(neighbors)

            # add the edge between the current cell and the neighboring cell
            edges.append((current_cell, neighbor))

            # move to the neighboring cell and mark it as visited
            current_cell = neighbor
            visited.add(current_cell)
        else:
            # backtrack to the previous cell
            current_cell = edges.pop()[0]

    # create a dictionary to store the edges
    graph = {cell: [] for cell in visited}
    for cell1, cell2 in edges:
        graph[cell1].append(cell2)
        graph[cell2].append(cell1)

    return graph

# generate the maze
maze = generate_maze(size)

# define the start and end points
start = (0, 0)
end = (size - 1, size - 1)

# define a dictionary to store the distances to each point
distances = {point: float('inf') for point in maze}
distances[start] = 0

# define a dictionary to store the previous point in the shortest path
previous = {point: None for point in maze}

# define a priority queue to store the points to visit
queue = [(0, start)]

# iterate over the priority queue
while queue:
    current_distance, current_point = heapq.heappop(queue)

    # check if the current point is the end point
    if current_point == end:
        break

    # iterate over the neighbors of the current point
    for neighbor in maze[current_point]:
        # calculate the distance to the neighbor
        distance = current_distance + 1

        # check if the distance to the neighbor is shorter than the current distance
        if distance < distances[neighbor]:
            distances[neighbor] = distance
            previous[neighbor] = current_point
            heapq.heappush(queue, (distance, neighbor))

# construct the shortest path
path = []
current_point = end
while current_point:
    path.append(current_point)
    current_point = previous[current_point]
path.reverse()

# print the shortest path and the distance to the end point
print('Shortest path:', path)
print('Distance:', distances[end])

