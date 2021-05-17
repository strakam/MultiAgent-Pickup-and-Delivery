import random, time, heapq
from pyglet import shapes
import pyglet as pg

# Check whether coordinates are in a grid
def ingrid(w, h, x, y):
        return x >= 0 and x < h and y >= 0 and y < w

class Package():
    packages_dropped, total_time, avg_time = 0, 0, 0
    avg, total = pg.text.Label, pg.text.Label

    @staticmethod
    def updateinfo(avg, total):
        Package.avg_time = round(Package.avg_time, 2)
        avg.text = "Average delivery time: " + str(Package.avg_time) + "s"
        total.text = "Packages delivered: " + str(Package.packages_dropped)

    def __init__(self, sx, sy, dx, dy, s, batch, grid):
        # x - horizontal, y - vertical, s - start, d - destination
        # sx - x coordinate of a starting position
        # dy - y coordinate of a destination position
        self.grid = grid
        self.sx, self.sy, self.dx, self.dy = sx, sy, dx, dy
        self.box = shapes.Rectangle((sy+0.15)*s, (sx+0.15)*s, 0.7*s, 0.7*s, 
                color=(255,0,200), batch=batch)
        self.deploytime = time.time()
        self.distances = []
        self.truedistance()

    # Compute distances from this package
    def truedistance(self):
        heap = [(0,self.sx, self.sy)]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.distances = [len(self.grid[0]) * [-1] for _ in range(len(self.grid))]
        self.distances[self.sx][self.sy] = 0
        while len(heap) > 0:
            pos = heapq.heappop(heap)
            # Compute possible moves
            for direction in directions:
                nx, ny = pos[1]+direction[0], pos[2]+direction[1]
                if ingrid(len(self.grid[0]), len(self.grid), nx, ny):
                    if (self.grid[nx][ny] == -4 or self.grid[nx][ny] == -3) and\
                            self.distances[nx][ny] == -1:
                        self.distances[nx][ny] = pos[0]+1
                        heapq.heappush(heap, (pos[0]+1, nx, ny))

    
    # Drop package to a random place in grid
    @staticmethod
    def droppackage(grid, s, batch):
        w, h = len(grid[0])-1, len(grid)-1
        while True:
            sx, sy = random.randint(0, h), random.randint(0, w)
            dx, dy = random.randint(0, h), random.randint(0, w)
            if grid[sx][sy] == -4:
                package = Package(sx, sy, dx, dy, s, batch, grid)
                grid[sx][sy] = -3
                return package

