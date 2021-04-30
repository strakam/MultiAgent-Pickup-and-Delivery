import random
from pyglet import shapes

class Package():
    packages_dropped, avg_time = 0, 0
    def __init__(self, sx, sy, dx, dy, s, batch):
        # x - horizontal, y - vertical
        self.sx, self.sy, self.dx, self.dy = sx, sy, dx, dy
        self.box = shapes.Rectangle((sy+0.15)*s, (sx+0.15)*s, 0.7*s, 0.7*s, 
                color=(0,255,0), batch=batch)
    
    # Drop package to a random place in grid
    @staticmethod
    def droppackage(grid, s, batch):
        w, h = len(grid[0])-1, len(grid)-1
        while True:
            sx, sy = random.randint(0, h), random.randint(0, w)
            dx, dy = random.randint(0, h), random.randint(0, w)
            if grid[sx][sy] == 0:
                package = Package(sx, sy, dx, dy, s, batch)
                grid[sx][sy] = -3
                return package

