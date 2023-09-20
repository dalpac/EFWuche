import pygame as pg
from editor import Editor

pg.init()

window = pg.display.set_mode((1100, 740))

class Demo:
    def start_demo():
        editor = Editor(1100, 740, window)
        editor.run()
        editor.load_level()

Demo.start_demo()
    