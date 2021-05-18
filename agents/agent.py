from pyglet import shapes
from queue import Queue
import simulator.controls as ctrl
import agents.package as p
import time, random, heapq

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
        for _ in range(40):
            sx = random.randint(0, len(Ai.grid)-1)
            sy = random.randint(0, len(Ai.grid[0])-1)
            Ai.agents.append(Ai.Agent(sx, sy, s, 16, ab, self))

    def act(self):
        for agent in Ai.agents:
            agent.move()
            if agent.tracker is True:
                agent.showintent()

    # assign package to an agent
    def assign(self, x, y):
        keys = list(Ai.packages.keys())
        if len(keys) > 0:
            return Ai.packages.pop(keys[0])
        return None
    
    # make all agents plan their trajectories
    def schedule():
        reservations = set()
        for agent in Ai.agents:
            agent.schedule(reservations)

    # constructor for agent
    class Agent():
        def __init__(self, x, y, s, speed, batch, Ai):
            self.x, self.y, self.s = x, y, s
            self.xfuel, self.yfuel, self.v = 0, 0, speed
            self.batch = batch
            self.color = (random.randint(0, 255),random.randint(0, 255),\
                    random.randint(0, 255))
            self.c = shapes.Circle(y*s + s/2, x*s + s/2, (s*0.8)//2, 
                    color=self.color, batch=batch)

            self.ai = Ai
            # queue for steps and tracker
            self.queue, self.trace = [], []
            self.task, self.tracker, self.button = None, True, ctrl.Button

        # transform from grid coordinates to drawing coordinates and move
        def move(self):
            if self.queue == []:
                if self.task is not None:
                    Ai.grid[self.x][self.y] = -4
                    p.Package.packages_dropped += 1               
                    p.Package.total_time += time.time() - self.task.deploytime
                    p.Package.avg_time = p.Package.total_time / p.Package.packages_dropped
                    self.task = None
                return
            s, inc = self.s, self.s/self.v
            if self.xfuel != 0:
                self.c.x += sign(self.xfuel)*inc
                self.xfuel -= sign(self.xfuel)*inc
            if self.yfuel != 0:
                self.c.y += sign(self.yfuel)*inc
                self.yfuel -= sign(self.yfuel)*inc
            if self.xfuel == 0 and self.yfuel == 0:
                coords = self.queue[0]
                self.queue.pop(0)
                step = (coords[1] - self.y, coords[0] - self.x)
                self.x, self.y = coords[0], coords[1]
                self.xfuel += s*step[0]
                self.yfuel += s*step[1]

        def schedule(self, reservations):
            if self.task is None:
                self.task = self.ai.assign(self.x, self.y)
            if self.task is not None:
                self.sta(self.task.sx, self.task.sy, reservations)

        # draw intended path
        def showintent(self):
            self.trace = []
            if self.button.state is True:
                f, t, o = self.c.x, self.c.y, self.s//2
                for i in range(len(self.queue)-1):
                    point = self.queue[i]
                    s = self.s
                    self.trace.append(shapes.Line(f, t, point[1]*s+o,
                        point[0]*s+o, color=self.color, width=2,
                            batch=self.batch))
                    f, t = point[1]*s+o, point[0]*s+o

        # spacetime astar
        def sta(self, tx, ty, reservations):
            # distances = self.task.distances
            # heap (prev,now,from x,from y, to x, to y)
            distances = self.task.distances
            d = distances[self.x][self.y]
            heap = [(d, d, self.x, self.y, self.x, self.y, 0)] 
            directions, steps = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)], {}
            found = False
            pos = None
            while len(heap) > 0:
                pos = heapq.heappop(heap)
                steps[(pos[6], pos[4], pos[5])] = (pos[6]-1, pos[2], pos[3])
                if pos[4] == tx and pos[5] == ty:
                    found = True
                    break
                # Compute possible moves
                for direction in directions:
                    nx, ny = pos[4]+direction[0], pos[5]+direction[1]
                    if ingrid(len(Ai.grid[0]), len(Ai.grid), nx, ny):
                        if (Ai.grid[nx][ny] == -4 or Ai.grid[nx][ny] == -3) and \
                                (pos[6]+1, nx,ny) not in reservations:
                            d = distances[nx][ny]
                            heapq.heappush(heap, (pos[1], d, pos[4],
                                pos[5], nx, ny, pos[6]+1))
            # backtrack and update info in reservation table
            if found:
                self.queue, que = [], []
                s = (pos[6], pos[4], pos[5])
                que.append(s)
                que.append(s)
                reservations.add(s)
                while steps[s] != s:
                    que.append(steps[s])
                    s = steps[s]
                    reservations.add(s)
                    reservations.add((s[0]-1, s[1], s[2]))
                    if s[1] == self.x and s[2] == self.y:
                        break
                que.append((0, self.x, self.y))
                for i in reversed(que):
                    self.queue.append((i[1], i[2]))


        # BFS for finding packages
        def plan(self, tx, ty, reservations):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            found = False
            q = Queue(0)
            q.put((self.x,self.y))
            visited = {(self.x, self.y) : (self.x, self.y)}
            while not q.empty():
                pos = q.get()
                # Closest package was reached
                if pos[0] == tx and pos[1] == ty:
                    # self.task = Ai.packages.pop((tx, ty))
                    found = True
                    break
                # Compute possible moves
                for direction in directions:
                    nx, ny = pos[0]+direction[0], pos[1]+direction[1]
                    if ingrid(len(Ai.grid[0]), len(Ai.grid), nx, ny):
                        if (Ai.grid[nx][ny] == -4 or Ai.grid[nx][ny] == -3) and\
                                (nx,ny) not in visited:
                            visited[(nx,ny)] = pos
                            q.put((nx,ny))

            # Get steps to package (backtrack BFS)
            if found:
                self.queue, que = [], []
                s = (tx,ty)
                que.append(s)
                que.append(s)
                while visited[s] != s:
                    que.append(visited[s])
                    s = visited[s]
                que.append((self.x, self.y))
                for i in reversed(que):
                    self.queue.append(i)
