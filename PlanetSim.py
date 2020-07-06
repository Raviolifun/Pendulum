# Model for generalized spring pendulum with wind resistance

# Standard
import math

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

# Required for updating the screen
@window.event
def on_draw():
    window.clear()
    main_batch.draw()
    # fps_display.draw()


# Moving the link
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global xPos, yPos
    if buttons & mouse.LEFT & (((-link.x + x)**2 + (-link.y + y)**2)**0.5 < 500):
        xPos = x
        yPos = y


# Function for centering objects
def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


# Batch of all objects (renders them in one go)
main_batch = pyglet.graphics.Batch()

# Objects to be batched. These create the pendulum seen on the screen

# x0, y0, vx0, vy0, mass
planet1 = Planet.Planet(window.get_size()[0] / 2,      window.get_size()[1] / 2, 0, 0, 6*(10**17),
                        batch=main_batch)
planet2 = Planet.Planet(window.get_size()[0] / 2 + 20, window.get_size()[1] / 2, 1, 0, 6*(10**17),
                        batch=main_batch)
planet3 = Planet.Planet(window.get_size()[0] / 2 - 200, window.get_size()[1] / 2, 0, -130, 6*(10**17),
                        batch=main_batch)
planet4 = Planet.Planet(window.get_size()[0] / 2, window.get_size()[1] / 2 + 240, -120, 0, 6*(10**17),
                        batch=main_batch)
planet5 = Planet.Planet(window.get_size()[0] / 2, window.get_size()[1] / 2 - 300, 110, 0, 6*(10**17),
                        batch=main_batch)
planet6 = Planet.Planet(window.get_size()[0] / 2, window.get_size()[1] / 2 - 400, 110, 0, 6*(10**17),
                        batch=main_batch)
planet7 = Planet.Planet(window.get_size()[0] / 2, window.get_size()[1] / 2 - 500, 110, 0, 6*(10**17),
                        batch=main_batch)
planet8 = Planet.Planet(window.get_size()[0] / 2, window.get_size()[1] / 2 - 600, 110, 0, 6*(10**17),
                        batch=main_batch)

planets = [planet1, planet2, planet3, planet4, planet5, planet6, planet7, planet8]
# planets = [planet1, planet2]

def update(dt):
    for planet in planets:
        planet.updateGravAccel(planets)

    dT = dt
    dtf = 1/100.0
    while dT > dtf:
        for planet in planets:
            planet.updatePosition(dtf)
        dT = dT - dtf
    for planet in planets:
        planet.updatePosition(dT)

    for planet in planets:
        if planet.x < 0:
            planet.vx = - planet.vx/100
            planet.x = 0
        if planet.x > window.get_size()[0]:
            planet.vx = - planet.vx / 100
            planet.x = window.get_size()[0]
        if planet.y < 0:
            planet.vy = - planet.vy/100
            planet.y = 0
        if planet.y > window.get_size()[1]:
            planet.vy = - planet.vy / 100
            planet.y = window.get_size()[1]


# Cause the clock update. This is what limits the precision of the simulation (step is is ~1/60)
pyglet.clock.schedule_interval(update, 1/60.0)

# Creates the window
pyglet.app.run()

