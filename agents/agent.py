from pyglet import shapes
import random

# Return sign of a given number
def sign(a):
    if a > 0:
        return 1
    return 0 if a == 0 else -1

class Agent():
    # constructor for agent
    def __init__(self, x, y, s, speed, batch):
        self.x, self.y, self.s = x, y, s
        self.xfuel, self.yfuel, self.v = 0, 0, speed
        self.c = shapes.Circle(x*s + s/2, y*s + s/2, (s*0.8)//2, 
                color=(255,0,0), batch=batch)
        self.queue = []
        for _ in range(100):
            self.queue.append(random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)]))

    # transform from grid coordinates to drawing coordinates and move
    def move(self):
        if len(self.queue) == 0:
            return
        s, inc = self.s, self.s/self.v
        if self.xfuel != 0:
            self.c.x += sign(self.xfuel)*inc
            self.xfuel -= sign(self.xfuel)*inc
        if self.yfuel != 0:
            self.c.y += sign(self.yfuel)*inc
            self.yfuel -= sign(self.yfuel)*inc
        if self.xfuel == 0 and self.yfuel == 0:
            step = self.queue[0]
            self.queue.pop(0)
            self.xfuel += s*step[0]
            self.yfuel += s*step[1]
