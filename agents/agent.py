from pyglet import shapes
import random
from queue import Queue

# Return sign of a given number
def sign(a):
    if a > 0:
        return 1
    return 0 if a == 0 else -1

# Check whether coordinates are in a grid
def ingrid(w, h, x, y):
        return x >= 0 and x < h and y >= 0 and y < w

class Ai():
    packages, agents, grid = dict(), [], []
    def __init__(self, ab, s):
        for _ in range(8):
            sx = random.randint(0, len(Ai.grid)-1)
            sy = random.randint(0, len(Ai.grid[0])-1)
            Ai.agents.append(Ai.Agent(sx, sy, s, 16, ab, self))

    def act(self):
        for agent in Ai.agents:
            agent.move()

    def assign(self, x, y):
        keys = list(Ai.packages.keys())
        if len(keys) > 0:
            p = keys[0]
            return p
        return (-1,-1)
    
    def schedule():
        for agent in Ai.agents:
            agent.askfortask()


    # constructor for agent
    class Agent():
        def __init__(self, x, y, s, speed, batch, Ai):
            self.x, self.y, self.s = x, y, s
            self.xfuel, self.yfuel, self.v = 0, 0, speed
            self.c = shapes.Circle(y*s + s/2, x*s + s/2, (s*0.8)//2, 
                    color=(255,0,0), batch=batch)
            self.ai = Ai
            # queue for steps
            self.queue = Queue(0)
            self.task = None

        # transform from grid coordinates to drawing coordinates and move
        def move(self):
            if self.queue.empty():
                if self.task is not None:
                    Ai.grid[self.x][self.y] = 0
                    # TODO call terminate for package later
                    self.task = self.askfortask()
                return
            s, inc = self.s, self.s/self.v
            if self.xfuel != 0:
                self.c.x += sign(self.xfuel)*inc
                self.xfuel -= sign(self.xfuel)*inc
            if self.yfuel != 0:
                self.c.y += sign(self.yfuel)*inc
                self.yfuel -= sign(self.yfuel)*inc
            if self.xfuel == 0 and self.yfuel == 0:
                coords = self.queue.get()
                step = (coords[1] - self.y, coords[0] - self.x)
                self.x, self.y = coords[0], coords[1]
                self.xfuel += s*step[0]
                self.yfuel += s*step[1]

        def askfortask(self):
            if self.task is None:
                sx, sy = self.ai.assign(self.x, self.y)
                if sx == -1 and sy == -1:
                    return
                self.plan(sx, sy)

        # BFS for finding packages
        def plan(self, tx, ty):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            found = False
            q = Queue(0)
            q.put((self.x,self.y))
            visited = {(self.x, self.y) : (self.x, self.y)}
            while not q.empty():
                pos = q.get()
                # Closest package was reached
                if pos[0] == tx and pos[1] == ty:
                    self.task = Ai.packages.pop((tx, ty))
                    found = True
                    break
                # Compute possible moves
                for direction in directions:
                    nx, ny = pos[0]+direction[0], pos[1]+direction[1]
                    if ingrid(len(Ai.grid[0]), len(Ai.grid), nx, ny):
                        if (Ai.grid[nx][ny] == 0 or Ai.grid[nx][ny] == -3) and\
                                (nx,ny) not in visited:
                            visited[(nx,ny)] = pos
                            q.put((nx,ny))
            # Get steps to package (backtrack BFS)
            if found:
                self.queue, que = Queue(0), []
                s = (tx,ty)
                que.append(s)
                que.append(s)
                while visited[s] != s:
                    que.append(visited[s])
                    s = visited[s]
                que.append((self.x, self.y))
                for i in reversed(que):
                    self.queue.put(i)

