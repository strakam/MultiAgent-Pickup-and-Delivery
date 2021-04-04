import easygraphics as eg

class Grid:
    # Constructor
    def __init__(self, squaresize, grid):
        self.grid, self.s = grid, squaresize
        self.w, self.h = len(self.grid[0]), len(self.grid)

        self.predrawgrid()

    # Draw current state of grid
    def drawgrid(self):
        eg.draw_image(0, 0, self.skeleton)

    # Predraw parts of the grid that doesn't change
    def predrawgrid(self):
        self.skeleton = eg.create_image(self.w*self.s, self.h*self.s)
        eg.set_target(self.skeleton)
        eg.set_color(eg.Color.BLACK)
        eg.set_fill_color(eg.color_rgb(0,0,0))
        # Draw obstacles
        for i in range(self.h):
            for j in range(self.w):
                if self.grid[i][j] == -1:
                    x, y, l = j*self.s, i*self.s, self.s
                    eg.fill_polygon(x, y, x+l, y, x+l, y+l, x, y+l)

        # Draw lines
        for i in range(self.w):
            eg.line(i*self.s, 0, i*self.s, self.s*self.h)

        for i in range(self.h):
            eg.line(0, i*self.s, self.w*self.s, i*self.s)


