import argparse
import simulator.simulator as sim
import pyglet as pg
import pyglet.shapes
import glooey
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


statics = pg.graphics.Batch()
env = sim.Grid(s, grid, statics)
window = pg.window.Window(len(grid[0])*s+300, len(grid)*s, caption='MAPD')

# Widgets
buttons, gui = ctrl.createbuttons(window, statics)

pg.gl.glClearColor(255, 255, 255, 1)

@window.event
def on_draw():
    window.clear()
    statics.draw()

if __name__ == "__main__":
    # Tell pyglet to do its thing
    pg.app.run()
