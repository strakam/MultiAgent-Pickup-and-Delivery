import easygraphics as eg
import argparse
import simulator.simulator as sim


def loadmap(filename):
    f = open(filename, "r")
    lines = f.readlines()
    grid = []
    for line in lines:
        grid.append([])
        for i in range(len(line)-1):
            x = 0 if line[i] == '.' else -1
            grid[len(grid)-1].append(x)
    return grid

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="filename of a saved grid")
    parser.add_argument("-s", "--squaresize", default=80, type=int, 
            help="size of one square in pixels")
    args = parser.parse_args()
    grid = []
    if args.file:
        grid = loadmap(args.file)
    eg.init_graph(len(grid[0])*args.squaresize, len(grid)*args.squaresize)
    eg.set_render_mode(eg.RenderMode.RENDER_MANUAL)
    d = sim.Grid(args.squaresize, grid)
    eg.set_target()
    while eg.is_run():
        if eg.delay_jfps(60):
            eg.clear_device()
            d.drawgrid()
    eg.close_graph()
eg.easy_run(main)
