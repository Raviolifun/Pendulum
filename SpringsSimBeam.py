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
    dx = x - SpringPoints[0].x
    dy = y - SpringPoints[0].y
    SpringPoints[0].x = SpringPoints[0].x + dx
    SpringPoints[0].y = SpringPoints[0].y + dy
    SpringPoints[1].x = SpringPoints[1].x + dx
    SpringPoints[1].y = SpringPoints[1].y + dy



@window.event
def on_mouse_release(x, y, button, modifiers):
    global x1, y1


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    dx = x - SpringPoints[0].x
    dy = y - SpringPoints[0].y
    SpringPoints[0].x = SpringPoints[0].x + dx
    SpringPoints[0].y = SpringPoints[0].y + dy
    SpringPoints[1].x = SpringPoints[1].x + dx
    SpringPoints[1].y = SpringPoints[1].y + dy

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
n = 50
k = 1000
c = 2
vxi = 0
vyi = 0
pos_x = 200
pos_y = 400
strut_length_x = 130/50*24
strut_length_y = 200
m = 10/n

"""
0# [2, 3] 2# [0, 1, 3, 4, 5] 4# [2, 3, 5, 6, 7] 6# [4, 5, 7, 8, 9] 8# [6, 7, 9, 10, 11] 10# [8, 9, 11, 12, 13] 12# [10, 11, 13, 14, 15] 14# [12, 13, 15]
1# [2, 3] 3# [0, 1, 2, 4, 5] 5# [2, 3, 4, 6, 7] 7# [4, 5, 6, 8, 9] 9# [6, 7, 8, 10, 11] 11# [8, 9, 10, 12, 13] 13# [10, 11, 12, 14, 15] 15# [12, 13, 14]
DON't update the position of 0 and 1 to make sure they are static
"""

# My Lazy way to do this... I need something to take an arbitrary shape and turn it into triangles -_-
SpringPoints = [None]*n
SpringPoints[0] = SpringPoint.SpringPoint(pos_x, pos_y, vxi, vyi, m, k, c, 2 + 1, color1=(0, 255, 0), batch=main_batch)
SpringPoints[0].neighbors_index = [2, 3]
SpringPoints[0].neighborsInitialDis = [strut_length_x] * 2
SpringPoints[1] = SpringPoint.SpringPoint(pos_x, pos_y + strut_length_y, vxi, vyi, m, k, c, 2 + 1, color1=(0, 255, 0), batch=main_batch)
SpringPoints[1].neighbors_index = [2, 3]
SpringPoints[1].neighborsInitialDis = [strut_length_x] * 2

for value in range((n-4)//2):
    SpringPoints[2 * value + 2] = SpringPoint.SpringPoint(pos_x + (value + 1) * strut_length_x, pos_y, vxi, vyi, m, k, c, 5 + 1, batch=main_batch)
    SpringPoints[2 * value + 3] = SpringPoint.SpringPoint(pos_x + (value + 1) * strut_length_x, pos_y + strut_length_y, vxi, vyi, m, k, c, 5 + 1, batch=main_batch)
    SpringPoints[2 * value + 2].neighborsInitialDis = [strut_length_x] * 5
    SpringPoints[2 * value + 3].neighborsInitialDis = [strut_length_x] * 5
    SpringPoints[2 * value + 2].neighbors_index = [2 * value, 2 * value + 1, 2 * value + 3, 2 * value + 4, 2 * value + 5]
    SpringPoints[2 * value + 3].neighbors_index = [2 * value, 2 * value + 1, 2 * value + 2, 2 * value + 4, 2 * value + 5]

SpringPoints[n-2] = SpringPoint.SpringPoint(pos_x + (n / 2 - 1)*strut_length_x, pos_y, vxi, vyi, m, k, c, 3 + 1, color1=(0, 255, 0), batch=main_batch)
SpringPoints[n-2].neighbors_index = [n-4, n-3, n-1]
SpringPoints[n-2].neighborsInitialDis = [strut_length_x] * 3
SpringPoints[n-1] = SpringPoint.SpringPoint(pos_x + (n / 2 - 1)*strut_length_x, pos_y + strut_length_y, vxi, vyi, m, k, c, 3 + 1, color1=(0, 255, 0), batch=main_batch)
SpringPoints[n-1].neighbors_index = [n-4, n-3, n-2]
SpringPoints[n-1].neighborsInitialDis = [strut_length_x] * 3

print(SpringPoints[0].neighbors_index)

for index in range(n):
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
        for value in range(n - 4):
            SpringPoints[value + 2].updateAccel(SpringPoints, 0, -9.8 * m * n)

        for value in range(n - 4):
            SpringPoints[value + 2].updatePosition(dtf, window.get_size()[0], window.get_size()[1])

        dT = dT - dtf

    for value in range(n - 4):
        SpringPoints[value + 2].updateAccel(SpringPoints,  0, -9.8 * m * n)

    for value in range(n - 4):
        SpringPoints[value + 2].updatePosition(dT, window.get_size()[0], window.get_size()[1])

    for value in range(n):
        SpringPoints[value].updateAnimation()


# Cause the clock update. This is what limits the precision of the simulation (step is is ~1/60)
pyglet.clock.schedule_interval(update, 1/60.0)

# Creates the window
pyglet.app.run()

