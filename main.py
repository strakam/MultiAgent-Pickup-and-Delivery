import argparse
import simulator.simulator as sim
import pyglet as pg
import simulator.controls as ctrl

def loadmap(filename):
    f = open(filename, "r")
    lines = f.readlines()
    grid = []
    for line in lines:
        grid.append([])
        for i in range(len(line)-1):
            x = 0 if line[i] == '.' else -1
            grid[len(grid)-1].append(x)
    f.close()
    return grid


# Parse command line input
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="filename of a saved grid")
parser.add_argument("-s", "--squaresize", default=80, type=int, 
        help="size of one square in pixels")
args = parser.parse_args()
s = args.squaresize
grid = []

# Create grid
if args.file:
    grid = loadmap(args.file)
else:
    grid = [10 * [0] for _ in range(10)]


statics, text = pg.graphics.Batch(), pg.graphics.Batch()
env = sim.Grid(s, grid, statics)
window = pg.window.Window(len(grid[0])*s+300, len(grid)*s, caption='MAPD')
buttons = ctrl.createbuttons(len(grid[0])*s+30, len(grid)*s - 60, statics, text)

pg.gl.glClearColor(255, 255, 255, 1)

@window.event
def on_draw():
    window.clear()
    statics.draw()
    text.draw()

@window.event
def on_mouse_motion(x, y, dx, dy):
    for b in buttons:
        b.hovered(x, y, statics)

@window.event
def on_mouse_press(x, y, button, modifiers):
    global env, window, buttons, statics, text
    for b in buttons:
        b.clicked(x, y)
        if b.text == "Load file" and b.state != "":
            grid = loadmap(b.state)
            statics, text = pg.graphics.Batch(), pg.graphics.Batch()
            env = sim.Grid(s, grid, statics)
            window.set_size(len(grid[0])*s+300, len(grid)*s)
            buttons = ctrl.createbuttons(len(grid[0])*s+30, len(grid)*s - 60, statics, text)
            b.state = ""

if __name__ == "__main__":
    pg.app.run()
