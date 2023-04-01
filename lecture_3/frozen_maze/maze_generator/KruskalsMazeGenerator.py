import random
import sys
import time

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
                #self.display_maze()
                #time.sleep(delay)

                set1.connect(set2)
                self.grid[y][x] |= direction
                self.grid[ny][nx] |= OPPOSITE[direction]

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
        

# maze = KruskalsMazeGenerate(width, height)
# maze.generate()
# print("\033[2J") # clear the screen
# maze.display_maze()

# print(maze.grid)

# 5. Show the parameters used to build this maze, for repeatability

#print(f"{sys.argv[0]} {width} {height} {seed}")