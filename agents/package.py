import random
from pyglet import shapes
import pyglet as pg
import time

class Package():
    packages_dropped, total_time, avg_time = 0, 0, 0
    avg, total = pg.text.Label, pg.text.Label

    @staticmethod
    def updateinfo(avg, total):
        Package.avg_time = round(Package.avg_time, 2)
        avg.text = "Average delivery time: " + str(Package.avg_time) + "s"
        total.text = "Packages delivered: " + str(Package.packages_dropped)

    def __init__(self, sx, sy, dx, dy, s, batch):
        # x - horizontal, y - vertical
        self.sx, self.sy, self.dx, self.dy = sx, sy, dx, dy
        self.box = shapes.Rectangle((sy+0.15)*s, (sx+0.15)*s, 0.7*s, 0.7*s, 
                color=(255,0,200), batch=batch)
        self.deploytime = time.time()
    
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

