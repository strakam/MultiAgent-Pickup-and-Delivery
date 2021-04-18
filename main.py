import argparse
import simulator.grid as sim
import simulator.controls as ctrl
import pyglet as pg
from agents import agent
from agents import package
from pyglet.window import mouse


# Load map and convert it
def loadmap(filename):
    f = open(filename, "r")
    lines = f.readlines()
    if lines[0] != "type octile\n":
        print("wrong map format")
        return []
    grid = []
    for j in range(4, len(lines)):
        grid.append([])
        line = lines[j]
        for i in range(len(line)-1):
            x = 0 
            if line[i] == '@':
                x = -2
            elif line[i] == 'T':
                x = -1
            elif line[i] == '.':
                x = 0
            else:
                x = -2
            grid[len(grid)-1].append(x)
    f.close()
    return grid


def move_agents(dt):
    for i in agents:
        i.move()


def droppackage(dt):
    for i in range(1):
        package.Package.droppackage(grid, s, ab)


# Parse command line input
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="filename of a saved grid")
parser.add_argument("-s", "--squaresize", default=20, type=int, 
        help="size of one square in pixels")
args = parser.parse_args()
s = args.squaresize
grid = []

# Create grid
if args.file:
    grid = loadmap(args.file)
else:
    grid = [80 * [0] for _ in range(80)]

statics, text, ab = pg.graphics.Batch(), pg.graphics.Batch(), pg.graphics.Batch()
env = sim.Grid(s, grid, statics)
window = pg.window.Window(len(grid[0])*s+300, len(grid)*s, caption='MAPD')
pg.gl.glClearColor(255, 255, 255, 1)
buttons = ctrl.createbuttons(len(grid[0])*s+30, len(grid)*s - 60, statics, text)

agents, packages = [], []
for i in range(3):
    agents.append(agent.Agent(20*(i+1), 20*(i+1), s, ab))

pg.clock.schedule_interval(move_agents, 0.01)
pg.clock.schedule_interval(droppackage, 5.0)

@window.event
def on_draw():
    window.clear()
    statics.draw()
    text.draw()
    ab.draw()


@window.event
def on_mouse_motion(x, y, dx, dy):
    for b in buttons:
        b.hovered(x, y, statics)


@window.event
def on_mouse_press(x, y, button, modifiers):
    global env, window, buttons, statics, text, grid
    for b in buttons:
        b.clicked(x, y)
        if b.text == "Load file" and b.state != ():
            grid = loadmap(b.state)
            statics, text = pg.graphics.Batch(), pg.graphics.Batch()
            env = sim.Grid(s, grid, statics)
            window.set_size(len(grid[0])*s+300, len(grid)*s)
            buttons = ctrl.createbuttons(len(grid[0])*s+30, 
                    len(grid)*s - 60, statics, text)
            b.state = ()
        if b.text == "Save file" and b.state != ():
            env.savetofile(b.state)
            b.state = ()
    if x < len(grid[0])*s and button == mouse.LEFT:
        env.togglesquare(x, y, -1)
    elif x < len(grid[0])*s and button == mouse.RIGHT:
        env.togglesquare(x, y, 0)
 

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if x < len(grid[0])*s and x > 0 and y > 0 and y < len(grid)*s:
        if x < len(grid[0])*s and buttons & mouse.LEFT:
            env.togglesquare(x, y, -1)
        elif x < len(grid[0])*s and buttons & mouse.RIGHT:
            env.togglesquare(x, y, 0)


if __name__ == "__main__":
    pg.app.run()
