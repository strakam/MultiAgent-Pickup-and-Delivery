import random
from pyglet import shapes

class Package():
    packages = []
    packages_dropped, avg_time = 0, 0
    def __init__(self, x, y, s, batch):
        self.x, self.y = x, y
        self.box = shapes.Rectangle((x+0.15)*s, (y+0.15)*s, 0.7*s, 0.7*s, 
                color=(222, 184, 135), batch=batch)
    
    @staticmethod
    def droppackage(grid, s, batch):
        w, h = len(grid[0])-1, len(grid)-1
        while True:
            x, y = random.randint(0, w), random.randint(0, h)
            if grid[y][x] == 0:
                grid[y][x] = Package(x, y, s, batch)
                return

