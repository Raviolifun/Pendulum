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
    SpringPoint9.x = x
    SpringPoint9.y = y


@window.event
def on_mouse_release(x, y, button, modifiers):
    global x1, y1


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    SpringPoint9.x = x
    SpringPoint9.y = y

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
n = 9
k = 10000
c = 0.1

SpringPoint1 = SpringPoint.SpringPoint(1112, 288, 1000, 1000, 9, k, c, n, batch=main_batch)
SpringPoint2 = SpringPoint.SpringPoint(688, 712, 1000, 1000, 9, k, c, n, batch=main_batch)
SpringPoint3 = SpringPoint.SpringPoint(688, 288, 1000, 1000, 9, k, c, n, batch=main_batch)
SpringPoint4 = SpringPoint.SpringPoint(1112, 712, 1000, 1000, 9, k, c, n, batch=main_batch)
SpringPoint5 = SpringPoint.SpringPoint(1200, 500, 1000, 1000, 9, k, c, n, batch=main_batch)
SpringPoint6 = SpringPoint.SpringPoint(600, 500, 1000, 1000, 9, k, c, n, batch=main_batch)
SpringPoint7 = SpringPoint.SpringPoint(900, 200, 1000, 1000, 9, k, c, n, batch=main_batch)
SpringPoint8 = SpringPoint.SpringPoint(900, 800, 1000, 1000, 9, k, c, n, batch=main_batch)
SpringPoint9 = SpringPoint.SpringPoint(900, 500, 1000, 1000, 9, k, c, n, color1=(0, 255, 0), batch=main_batch)
SpringPoints = [SpringPoint1, SpringPoint2, SpringPoint3, SpringPoint4, SpringPoint5, SpringPoint6, SpringPoint7,
                SpringPoint8, SpringPoint9]

currentSpring = 0
neighbors = range(n)
for SpringPoint in SpringPoints:
    #currentSpring = 0
    #neighbors = [1, 2, 3]
    neighbors_star = []

    # Filter out self from neighbor list
    for neighbor in neighbors:
        if neighbor != currentSpring:
            neighbors_star.append(neighbor)
    SpringPoint.neighbors_index = neighbors_star

    i = 0
    for neighbor in neighbors_star:
        dx = SpringPoints[neighbor].x - SpringPoints[currentSpring].x
        dy = SpringPoints[neighbor].y - SpringPoints[currentSpring].y
        SpringPoint.neighborsInitialDis[i] = (dx**2 + dy**2)**0.5
        i = i + 1

    # Update Self Filter
    currentSpring = currentSpring + 1


def update(dt):
    dT = dt
    dtf = 1/60
    while dT > dtf:
        for SpringPoint in SpringPoints:
            SpringPoint.updateAccel(SpringPoints, 0, 0)

        for SpringPoint in SpringPoints:
            SpringPoint.updatePosition(dtf, window.get_size()[0], window.get_size()[1])

        dT = dT - dtf

    for SpringPoint in SpringPoints:
        SpringPoint.updateAccel(SpringPoints,  0, 0)

    for SpringPoint in SpringPoints:
        SpringPoint.updatePosition(dT, window.get_size()[0], window.get_size()[1])
        SpringPoint.updateAnimation()


# Cause the clock update. This is what limits the precision of the simulation (step is is ~1/60)
pyglet.clock.schedule_interval(update, 1/60.0)

# Creates the window
pyglet.app.run()

