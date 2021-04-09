import glooey
import tkinter as tk
from tkinter import filedialog

class ButtonLabel(glooey.Label):
    custom_color = '#babdb6'
    custom_font_size = 20
    custom_alignment = 'center'

class Button(glooey.Button):
    Foreground = ButtonLabel
    custom_alignment = 'fill'
    custom_width_hint = 140
    custom_height_hint = 60 
    custom_bottom_padding = 20
    custom_right_padding = 80

    class Base(glooey.Background):
        custom_color = '#204a87'

    class Over(glooey.Background):
        custom_color = '#3465a4'

    class Down(glooey.Background):
        custom_color = '#729fcff'

    def __init__(self, text):
        super().__init__(text)

    def on_click(self, widget):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()
        print(file_path)

def createbuttons(window, statics):
    buttons = [
                Button("Pause"),
                Button("Load file"),
                Button("Save file"),
                Button("Record")
              ]
    gui = glooey.Gui(window, batch=statics)
    vbox = glooey.VBox()
    vbox.alignment="top right"
    for button in buttons:
        vbox.add(button)
    gui.add(vbox)
    return buttons, gui
