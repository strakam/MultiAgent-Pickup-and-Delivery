import tkinter as tk
import pyglet as pg
from pyglet import shapes
from tkinter import filedialog
from agents import agent as ag

class Button():
    def __init__(self, x, y, a, b, c, text, statics, textbatch=None):
        self.text, self.state = text, ()
        if self.text == "":
            self.state = False
        self.w, self.h, self.x, self.y = a, b, x, y
        self.border_color = (0,0,0)
        self.label = pg.text.Label(self.text, x=x+50, y=y+25,
                color=(0,0,0,255), anchor_x='center', anchor_y='center', 
                batch=textbatch, font_size=15, font_name='Times New Roman')

        self.rect = shapes.BorderedRectangle(x, y, self.w, self.h, color=c,
                border_color=self.border_color, batch=statics)

    # Perform button action when it is clicked
    def clicked(self, x, y):
        if self.inside(x, y):
            if self.text == "Load file":
                root = tk.Tk()
                root.withdraw()
                self.state = filedialog.askopenfilename()
            elif self.text == "Save file":
                root = tk.Tk()
                root.withdraw()
                self.state = filedialog.asksaveasfilename()
            elif self.text == "":
                self.state = not self.state

    # Change border when hovered
    def hovered(self, x, y, statics):
        bc = self.border_color
        if self.inside(x, y):
            self.border_color = (255,0,0)
        else:
            self.border_color = (0,0,0)
        if bc != self.border_color:
            self.rect = shapes.BorderedRectangle(self.x, self.y, self.w, self.h,
                    border_color=self.border_color, batch=statics)

    # Check whether mouse is in a button area
    def inside(self, x, y):
        return x >= self.x and x <= self.x+self.w and y >= self.y\
                and y <= self.y+self.h

def createbuttons(x, y, statics, tb, ai):
    buttons, text = [], ["Pause", "Load file", "Save file", "Record"]
    margin = -40
    for i in range(4):
        c = (255,255,255)
        buttons.append(Button(x, y - (i*60), 100, 50, c, text[i], statics, tb))
    y -= 250
    for i in range(len(ai.agents)):
        margin += 40
        if x + margin > x + 200:
            margin = 0
            y -= 60
        c = ai.agents[i].color
        ai.agents[i].button = Button(x+margin, y, 30, 30, c, "", statics, tb)
    return buttons
