import random
import sys
import heapq
import pprint

# 1. Allow the maze to be customized via command-line parameters

width  = int(sys.argv[1]) if len(sys.argv) > 1 else 10
height = int(sys.argv[2]) if len(sys.argv) > 2 else width
seed   = int(sys.argv[3]) if len(sys.argv) > 3 else random.randint(0, 0xFFFF_FFFF)
delay  = float(sys.argv[4]) if len(sys.argv) > 4 else 0.01

random.seed(seed)

# 2. Set up constants to aid with describing the passage directions
N, S, E, W = 1, 2, 4, 8
DX         = { E: 1, W: -1, N:  0, S: 0 }
DY         = { E: 0, W:  0, N: -1, S: 1 }
OPPOSITE   = { E: W, W:  E, N:  S, S: N }


# 3. Data structures and methods to assist the algorithm

    # --------------------------------------------------------------------
# 6. Dijkstra's algorithm for solving the maze
# --------------------------------------------------------------------

# A priority queue implementation, adapted from https://gist.github.com/joninvski/701720

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

    def decrease_key(self, item, priority):
        for i, (p, e) in enumerate(self.elements):
            if e == item and p > priority:
                del self.elements[i]
                heapq.heappush(self.elements, (priority, item))
                break


class Tree:
    def __init__(self) -> None:
        self.parent = None

    def root(self):
        return self if self.parent is None else self.parent.root()

    def connected(self, tree) -> bool:
        return self.root() == tree.root()

    def connect(self, tree):
        tree.root().parent = self

class KruskalsMazeGenerate:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.edges = []
        self._create_edges()
        self.grid = [[0] * self.width for _ in range(self.height)]
        self.sets = [[Tree() for _ in range(self.width)] for _ in range(self.height)]
        self.walls = {i : {'N': 1 if i in range(width) else 0, 'S': 0, 'W': 1 if (i + width ) % width == 0 else 0, 'E': 0} for i in range(width * height)}
        self.generate()
        self.build_walls()
        self.path = self.find_path(self.state_to_point(0), self.state_to_point((width * height) - 1))

    # build the list of edges
    def _create_edges(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if y > 0:
                    self.edges.append((x, y, N))
                if x > 0:
                    self.edges.append((x, y, W))

    # 4. Kruskal's algorithm
    def generate(self) -> None:
        random.shuffle(self.edges)

        while self.edges:
            x, y, direction = self.edges.pop()
            nx, ny = x + DX[direction], y + DY[direction]

            set1, set2 = self.sets[y][x], self.sets[ny][nx]

            if not set1.connected(set2):
                set1.connect(set2)
                self.grid[y][x] |= direction
                self.grid[ny][nx] |= OPPOSITE[direction]

    def build_walls(self) -> None:
        i, j = (0, 0)
        for row in self.grid:
            for cell in row:
                state = i * self.width + j
                if cell & S != 0:
                    self.walls[state]['S'] = 0
                else:
                    self.walls[state]['S'] = 1
                    if i < self.height - 1:
                        self.walls[state + self.width]['N'] = 1

                # print(" " if cell & S != 0 else "_", end="")
                if cell & E != 0:
                    if (cell | row[row.index(cell)+1]) & S != 0:
                        if self.walls[state]['S'] != 1:
                            self.walls[state]['S'] = 0
                    else:
                        self.walls[state]['S'] = 1
                        if i < self.height - 1:
                            self.walls[state + self.width]['N'] = 1
                    # print(" " if (cell | row[row.index(cell)+1]) & S != 0 else "_", end="")
                else:
                    self.walls[state]['E'] = 1
                    if state < (self.width * self.height) - 1:
                        self.walls[state + 1]['W'] = 1
                    # print("|", end="")
                j += 1
            j = 0
            i += 1

    #find the way in the grid perceiving the walls
    def find_path(self, start, goal):
        costs = [[float('inf')] * self.width for _ in range(self.height)]
        costs[start[1]][start[0]] = 0
        visited = [[False] * self.width for _ in range(self.height)]
        pq = [(0, start)]
        path = {}

        while pq:
            current_cost, current = heapq.heappop(pq)
            if current == goal:
                break
            if visited[current[1]][current[0]]:
                continue
            visited[current[1]][current[0]] = True

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx, ny = current[0] + dx, current[1] + dy
                if nx < 0 or ny < 0 or nx >= self.width or ny >= self.height or visited[ny][nx]:
                    continue

                # Check if there is a wall between the current node and its neighbor
                if dx == 1 and self.walls[current[1] * self.width + current[0]]["E"] == 1:
                    continue
                elif dx == -1 and self.walls[current[1] * self.width + nx]["E"] == 1:
                    continue
                elif dy == 1 and self.walls[current[1] * self.width + current[0]]["S"] == 1:
                    continue
                elif dy == -1 and self.walls[ny * self.width + current[0]]["S"] == 1:
                    continue

                cost = current_cost + 1
                if (self.grid[current[1]][current[0]] & E and dx == 1) or \
                (self.grid[current[1]][current[0]] & S and dy == 1) or \
                (nx > 0 and self.grid[ny][nx - 1] & E and dx == -1) or \
                (ny > 0 and self.grid[ny - 1][nx] & S and dy == -1):
                    cost += 1

                if cost < costs[ny][nx]:
                    costs[ny][nx] = cost
                    heapq.heappush(pq, (cost, (nx, ny)))
                    path[(ny, nx)] = (current[1], current[0])

        if goal not in path:
            return None

        # Reconstruct the path
        node = goal
        path_array = [node]
        while node != start:
            node = path[node]
            path_array.append(node)

        return [self.point_to_state(point) for point in path_array[::-1]]

    def display_maze(self) -> None:
        print("\033[H") # move to upper-left
        print(" " + "_" * (len(self.grid[0]) * 2 - 1))
        for row in self.grid:
            print("|", end="")
            for cell in row:
                if cell == 0:
                    print("\033[47m", end="")
                print(" " if cell & S != 0 else "_", end="")
                if cell & E != 0:
                    print(" " if (cell | row[row.index(cell)+1]) & S != 0 else "_", end="")
                else:
                    print("|", end="")
                if cell == 0:
                    print("\033[m", end="")
            print()

    def point_to_state(self, point):
        return point[0] * self.width + point[1]
    
    def state_to_point(self, state):
        return (state // self.width, state % self.width)


    

# Find a path from the top-left corner of the maze to the bottom-right corner
# print("Finding path...")
# dijkstra(grid, (0, 0), (width - 1, height - 1))

# Display the maze with the path highlighted
# print("Displaying path...")
# display_maze(grid)

 

maze = KruskalsMazeGenerate(4, 4)
print("\033[2J") # clear the screen
# # path = maze.dijkstra((0, 0), (2, 2))
# # print('path = ', path)
#maze.display_maze()
# maze.build_walls()

# print('Aqui estoy')
# maze.find_path((0, 0), (3, 3))

# pprint.pprint(maze.state_to_point(15))
# 5. Show the parameters used to build this maze, for repeatability

# print(f"{sys.argv[0]} {width} {height} {seed}")