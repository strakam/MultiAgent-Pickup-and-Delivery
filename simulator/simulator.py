from pyglet import shapes

class Grid:
    # Constructor
    def __init__(self, squaresize, grid, statics):
        self.grid, self.s = grid, squaresize
        self.w, self.h = len(self.grid[0]), len(self.grid)
        self.lines, self.blocks = [], []

        # Create grid
        for i in range(self.w+1):
            self.lines.append(shapes.Line(self.s*i, 0, self.s*i,
                len(self.grid)*self.s, color=(0,0,0), batch=statics))
        for i in range(self.h):
            self.lines.append(shapes.Line(0, self.s*i, len(self.grid[0])*self.s,
                self.s*i, color=(0,0,0), batch=statics))

        self.grid.reverse()
        for i in range(self.h):
            for j in range(self.w):
                if self.grid[i][j] == -1:
                    x, y, l = j*self.s, i*self.s, self.s
                    self.blocks.append(shapes.Rectangle(x, y, l, l,
                        color=(0,0,0), batch=statics))

