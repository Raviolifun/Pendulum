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
import Link
import MotionFade
import Planet
import Graph

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
x1, y1, x2, y2 = 0, 0, 0, 0
planetMassE = 7

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
    global x1, y1
    x1 = x
    y1 = y


@window.event
def on_mouse_release(x, y, button, modifiers):
    global planets, x1, y1, x2, y2
    planets = np.append(planets, Planet.Planet(x, y, (x2 - x1), (y2 - y1), 10000000*(10**planetMassE), batch=main_batch))


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global x2, y2
    x2 = x
    y2 = y

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global planetMassE
    planetMassE = planetMassE + scroll_y


# Function for centering objects
def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


# Batch of all objects (renders them in one go)
main_batch = pyglet.graphics.Batch()

# Objects to be batched. These create the pendulum seen on the screen

# x0, y0, vx0, vy0, mass

planets = [None] * 40

for val in range(40):
    planets[val] = Planet.Planet(random.uniform(1, 2000), random.uniform(1, 1000),
                                 1 - random.uniform(1, 2), 1 - random.uniform(1, 2),
                                 random.uniform(1, 1000000)*(10**10), batch=main_batch)


# planet1 = Planet.Planet(window.get_size()[0] / 2,      window.get_size()[1] / 2, 0, 0, 6*(10**15),
#                        batch=main_batch)
# planet2 = Planet.Planet(window.get_size()[0] / 2 + 200, window.get_size()[1] / 2, 0, 0, 6*(10**15),
#                        batch=main_batch)

# planets = [planet1, planet2]

def update(dt):


    dT = dt
    dtf = 1/60
    while dT > dtf:
        for planet in planets:
            planet.updateGravAccel(planets)

        for planet in planets:
            planet.updatePosition(dtf)

        dT = dT - dtf

    for planet in planets:
        planet.updateGravAccel(planets)
    for planet in planets:
        planet.updatePosition(dT)
        planet.updateAnimation()

    """
    for planet in planets:
        if planet.x < 0:
            planet.vx = - planet.vx
            planet.x = 0
        elif planet.x > window.get_size()[0]:
            planet.vx = - planet.vx
            planet.x = window.get_size()[0]
        elif planet.y < 0:
            planet.vy = - planet.vy
            planet.y = 0
        elif planet.y > window.get_size()[1]:
            planet.vy = - planet.vy
            planet.y = window.get_size()[1]
    """

    """
    dampFact = 1
    for planet in planets:
        if planet.x < 0:
            planet.vx = planet.vx / dampFact
            planet.x = window.get_size()[0]
        elif planet.x > window.get_size()[0]:
            planet.vx = planet.vx / dampFact
            planet.x = 0
        elif planet.y < 0:
            planet.vy = planet.vy / dampFact
            planet.y = window.get_size()[1]
        elif planet.y > window.get_size()[1]:
            planet.vy = planet.vy / dampFact
            planet.y = 0"""


# Cause the clock update. This is what limits the precision of the simulation (step is is ~1/60)
pyglet.clock.schedule_interval(update, 1/60.0)

# Creates the window
pyglet.app.run()

