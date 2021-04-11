import tkinter as tk
import pyglet as pg
from pyglet import shapes
from tkinter import filedialog

class Button():
    def __init__(self, x, y, text, statics, textbatch):
        self.text, self.state = text, ()
        self.w, self.h, self.x, self.y = 100, 50, x, y
        self.border_color = (0,0,0)
        self.label = pg.text.Label(self.text, x=x+50, y=y+25,
                color=(0,0,0,255), anchor_x='center', anchor_y='center', 
                batch=textbatch, font_size=15, font_name='Times New Roman')

        self.rect = shapes.BorderedRectangle(x, y, self.w, self.h,
                border_color=self.border_color, batch=statics)

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
            else:
                self.state = self.text

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

    def inside(self, x, y):
        return x >= self.x and x <= self.x+self.w and y >= self.y\
                and y <= self.y+self.h

def createbuttons(x, y, statics, tb):
    buttons, text = [], ["Pause", "Load file", "Save file", "Record"]
    for i in range(4):
        buttons.append(Button(x, y - i*60, text[i], statics, tb))
    return buttons
