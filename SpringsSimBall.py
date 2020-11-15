# Model for generalized spring pendulum with wind resistance

# Standard
import math
import random
import numpy as np
import time

# Libraries
import pyglet
from pyglet.window import mouse
from pyglet.window import key
from pyglet import shapes

# Application Specific
import SpringPoint


# Setup for limiting the window size, adding icons, and adding an FPS display
window = pyglet.window.Window(1920, 950, caption='Simulation of Pendulum', resizable=True)
window.set_minimum_size(320, 200)
window.set_maximum_size(1920, 1080)
icon1 = pyglet.image.load('.\\resources\\Bee.png')
icon2 = pyglet.image.load('.\\resources\\Bee32.png')
window.set_icon(icon1, icon2)
fps_display = pyglet.window.FPSDisplay(window=window)

# For size adjustment
pixelsPerMeter = 10
xPos = window.get_size()[0] / 2
yPos = window.get_size()[1] / 2
x1, y1, x2, y2, = 0, 0, 0, 0

# For code timing
# tOne = time.perf_counter()
# tTwo = time.perf_counter()

# Required for updating the screen
@window.event
def on_draw():
    window.clear()
    main_batch.draw()
    # fps_display.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    dx = x - SpringPoints[n-1].x
    dy = y - SpringPoints[n-1].y
    for SpringPoint in SpringPoints:
        SpringPoint.x = SpringPoint.x + dx
        SpringPoint.y = SpringPoint.y + dy



@window.event
def on_mouse_release(x, y, button, modifiers):
    global x1, y1


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    dx = x - SpringPoints[n-1].x
    dy = y - SpringPoints[n-1].y
    for SpringPoint in SpringPoints:
        SpringPoint.x = SpringPoint.x + dx
        SpringPoint.y = SpringPoint.y + dy

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global x1


# Function for centering objects
def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


# Batch of all objects (renders them in one go)
main_batch = pyglet.graphics.Batch()

# Objects to be batched. These create the pendulum seen on the screen

# x0, y0, vx0, vy0, mass

# Current *bug not really* is that they cannot have different k or c values
n = 40
k = 400
c = 2
vxi = 0
vyi = 0
pos_x = 900
pos_y = 500
radius = 400
m = 20/n

SpringPoints = [None]*n
SpringPoints[n - 1] = SpringPoint.SpringPoint(pos_x, pos_y, vxi, vyi, m, k, c, n, color1=(0, 255, 0), batch=main_batch)
SpringPoints[n - 1].neighbors_index = range(n - 1)
SpringPoints[n - 1].neighborsInitialDis = [radius] * (n - 1)

angle_dif = 2*math.pi/(n-1)
angle = 0
for index in range(n-1):
    point_x = pos_x + math.cos(angle) * radius
    point_y = pos_y + math.sin(angle) * radius

    SpringPoints[index] = SpringPoint.SpringPoint(point_x, point_y, vxi, vyi, m, k, c, 5 + 1, batch=main_batch)

    zeroth_index = (index + n - 3) % (n - 1)
    first_index = (index + n - 2) % (n-1)
    second_index = (index + 1) % (n-1)
    third_index = (index + 2) % (n - 1)

    neighbors = [n - 1, zeroth_index, first_index, second_index, third_index]


    SpringPoints[index].neighbors_index = neighbors
    print(SpringPoints[index].neighbors_index)

    angle = angle + angle_dif

for index in range(n-1):
    i = 0
    for neighbor in SpringPoints[index].neighbors_index:
        dx = SpringPoints[neighbor].x - SpringPoints[index].x
        dy = SpringPoints[neighbor].y - SpringPoints[index].y
        SpringPoints[index].neighborsInitialDis[i] = (dx**2 + dy**2)**0.5
        i = i + 1


def update(dt):

    dT = dt
    dtf = 1/120
    while dT > dtf:
        for SpringPoint in SpringPoints:
            SpringPoint.updateAccel(SpringPoints, 0, -9.8 * m * n)

        for SpringPoint in SpringPoints:
            SpringPoint.updatePosition(dtf, window.get_size()[0], window.get_size()[1])

        dT = dT - dtf

    for SpringPoint in SpringPoints:
        SpringPoint.updateAccel(SpringPoints,  0, -9.8 * m * n)

    for SpringPoint in SpringPoints:
        SpringPoint.updatePosition(dT, window.get_size()[0], window.get_size()[1])
        SpringPoint.updateAnimation()


# Cause the clock update. This is what limits the precision of the simulation (step is is ~1/60)
pyglet.clock.schedule_interval(update, 1/60.0)

# Creates the window
pyglet.app.run()

