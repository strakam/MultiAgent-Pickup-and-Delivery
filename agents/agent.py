from pyglet import shapes
from queue import Queue

# Return sign of a given number
def sign(a):
    if a > 0:
        return 1
    return 0 if a == 0 else -1

class Agent():
    packages = dict()
    # constructor for agent
    def __init__(self, x, y, s, speed, batch):
        self.x, self.y, self.s = x, y, s
        self.xfuel, self.yfuel, self.v = 0, 0, speed
        self.c = shapes.Circle(x*s + s/2, y*s + s/2, (s*0.8)//2, 
                color=(255,0,0), batch=batch)
        # queue for steps
        self.queue = Queue(0)
        self.task = None

    # transform from grid coordinates to drawing coordinates and move
    def move(self, grid):
        if self.queue.empty():
            if self.task is not None:
                Agent.packages.pop((self.x, self.y))
                self.task = None
                grid[self.x][self.y] = 0
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

    # BFS for finding packages
    def plan(self, grid):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        found = False
        q = Queue(0)
        tx, ty = self.x, self.y
        q.put((self.x,self.y))
        visited = {(self.x, self.y) : (self.x, self.y)}
        while not q.empty():
            pos = q.get()
            if grid[pos[0]][pos[1]] == -3:
                tx, ty = pos[0], pos[1]
                self.task = Agent.packages[(tx,ty)]
                found = True
                break
            for direction in directions:
                nx, ny = pos[0]+direction[0], pos[1]+direction[1]
                if ingrid(len(grid[0]), len(grid), nx, ny):
                    if (grid[nx][ny] == 0 or grid[nx][ny] == -3) and (nx,ny) not in visited:
                        visited[(nx,ny)] = pos
                        q.put((nx,ny))
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

def ingrid(w, h, x, y):
        return x >= 0 and x < h and y >= 0 and y < w
