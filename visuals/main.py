from p5 import *

def setup():
    size(800, 600)
    background(255)

def draw():
    fill(255, 0, 0)
    circle((mouse_x, mouse_y), 50)

run()
