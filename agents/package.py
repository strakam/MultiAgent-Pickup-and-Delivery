import random
from pyglet import shapes

class Package():
    packages_dropped, avg_time = 0, 0
    def __init__(self, x, y, s, batch):
        # x - horizontal, y - vertical
        self.x, self.y = x, y
        self.box = shapes.Rectangle((y+0.15)*s, (x+0.15)*s, 0.7*s, 0.7*s, 
                color=(0,255,0), batch=batch)
    
    # Drop package to a random place in grid
    @staticmethod
    def droppackage(grid, s, batch):
        w, h = len(grid[0])-1, len(grid)-1
        while True:
            x, y = random.randint(0, h), random.randint(0, w)
            if grid[x][y] == 0:
                package = Package(x, y, s, batch)
                grid[x][y] = -3
                return package

