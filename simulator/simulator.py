from pyglet import shapes

class Grid:
    # Constructor
    def __init__(self, squaresize, grid, statics):
        self.grid, self.s = grid, squaresize
        self.w, self.h = len(self.grid[0]), len(self.grid)
        self.lines, self.blocks = [], []
        self.statics = statics

        # Create grid
        self.grid.reverse()
        self.drawgrid()

    def togglesquare(self, x, y, block):
        x1, y1 = y//self.s, x//self.s
        prev = self.grid[x1][y1]
        self.grid[x1][y1] = block
        if prev != block:
            self.drawgrid()
    
    def drawgrid(self):
        for i in range(self.h):
            for j in range(self.w):
                x, y, l = j*self.s, i*self.s, self.s
                color=(255,255,255)
                if self.grid[i][j] == -1:
                    color=(0,0,0)
                elif self.grid[i][j] == -2:
                    color = (255, 0, 0)
                self.blocks.append(shapes.Rectangle(x, y, l, l,
                    color=color, batch=self.statics))

        for i in range(self.w+1):
            self.lines.append(shapes.Line(self.s*i, 0, self.s*i,
                len(self.grid)*self.s, color=(0,0,0), batch=self.statics))
        for i in range(self.h):
            self.lines.append(shapes.Line(0, self.s*i, len(self.grid[0])*self.s,
                self.s*i, color=(0,0,0), batch=self.statics))

    def savetofile(self, filename):
        rev = []
        for i in reversed(self.grid):
            rev.append(i)

        f = open(filename, "w")
        for i in range(self.h):
            line = ""
            for j in range(self.w):
                if rev[i][j] == -1:
                    line += '#'
                elif rev[i][j] == 0:
                    line += '.'
            f.write(line + '\n')
        f.close()

