import argparse
import simulator.grid as sim
import simulator.controls as ctrl
import pyglet as pg
from agents import agent
import agents.package as pkgs
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
            x = -4
            if line[i] == '@':
                x = -2
            elif line[i] == 'T':
                x = -1
            elif line[i] == '.':
                x = -4
            else:
                x = -2
            grid[len(grid)-1].append(x)
    f.close()
    return grid


# move agents every 10ms
def move_agents(dt):
    ai.act()
pg.clock.schedule_interval(move_agents, 0.01)


# drop packages in a given time interval -- current 5s
def drop_package(dt):
    pkg = pkgs.Package.droppackage(grid, s, ab)
    agent.Ai.packages[(pkg.sx, pkg.sy)] = pkg
    agent.Ai.schedule()
pg.clock.schedule_interval(drop_package, 2.0)


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
    grid = [50 * [-4] for _ in range(50)]

statics, text, ab = pg.graphics.Batch(), pg.graphics.Batch(), pg.graphics.Batch()
env = sim.Grid(s, grid, statics)
window = pg.window.Window(len(grid[0])*s+300, len(grid)*s, caption='MAPD')
pg.gl.glClearColor(255, 255, 255, 1)
agent.Ai.grid = grid
ai = agent.Ai(ab, s)
buttons = ctrl.createbuttons(len(grid[0])*s+30, len(grid)*s - 60, statics, text,
        ai)

# Information displays
avg = pg.text.Label("Average delivery time: " + str(pkgs.Package.avg_time)+ "s",
        x = len(grid[0])*s+133, y = len(grid)*s - 270, color=(0,0,0,255),
        batch=text,
        anchor_x='center', anchor_y='center', font_size=15, font_name='Times New Roman')

total = pg.text.Label("Packages delivered: " +
        str(pkgs.Package.packages_dropped),
        x = len(grid[0])*s+117, y = len(grid)*s - 300, color=(0,0,0,255),
        batch=text,
        anchor_x='center', anchor_y='center', font_size=15, font_name='Times New Roman')

@window.event
def on_draw():
    pkgs.Package.updateinfo(avg, total)
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
                    len(grid)*s - 60, statics, text, ai)
            b.state = ()
        if b.text == "Save file" and b.state != ():
            env.savetofile(b.state)
            b.state = ()
    for ag in ai.agents:
        ag.button.clicked(x, y)
    if x < len(grid[0])*s and button == mouse.LEFT:
        env.togglesquare(x, y, -1)
    elif x < len(grid[0])*s and button == mouse.RIGHT:
        env.togglesquare(x, y, -4)
 

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if x < len(grid[0])*s and x > 0 and y > 0 and y < len(grid)*s:
        if x < len(grid[0])*s and buttons & mouse.LEFT:
            env.togglesquare(x, y, -1)
        elif x < len(grid[0])*s and buttons & mouse.RIGHT:
            env.togglesquare(x, y, -4)


if __name__ == "__main__":
    pg.app.run()
