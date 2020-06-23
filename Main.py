# Model for a basic pendulum

# Standard
import math

# Libraries
import pyglet
from pyglet.window import key
from pyglet import shapes

# Application Specific
# (place holder)

# Setup for limiting the window size, adding icons, and adding an FPS display
window = pyglet.window.Window(900, 700, caption='Simulation of Pendulum', resizable=True, )
window.set_minimum_size(320, 200)
window.set_maximum_size(1024, 768)
icon1 = pyglet.image.load('.\\resources\\Bee.png')
icon2 = pyglet.image.load('.\\resources\\Bee32.png')
window.set_icon(icon1, icon2)
fps_display = pyglet.window.FPSDisplay(window=window)


# Required for updating the screen
@window.event
def on_draw():
    window.clear()
    main_batch.draw()
    fps_display.draw()


# Key event example to move window
@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        x, y = window.get_location()
        window.set_location(x + 20, y)


# Function for centering objects
def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


# Batch of all objects (renders them in one go)
main_batch = pyglet.graphics.Batch()

# Objects to be batched. These create the pendulum seen on the screen
circle = shapes.Circle(x=0, y=0, radius=25, color=(225, 225, 225), batch=main_batch)
circleTwo = shapes.Circle(x=0, y=0, radius=25, color=(225, 225, 225), batch=main_batch)
rectangle = shapes.Rectangle(x=0, y=0, width=30, height=200, color=(225, 225, 225), batch=main_batch)

# This allows the rectangle to be easily pivoted by the center of its top side
rectangle._anchor_x = rectangle.width/2
rectangle._anchor_y = rectangle.height

# Function Constants
g = 9.81
r = 10

# Initialisation Constants
thetaVal = 2
thetaVald = 0
thetaValdd = 1.5


def update(dt):
    # The Dynamic System: x'' * r - g * sin(x) = 0

    # Force these to be global rather than local
    global thetaVal, thetaVald, thetaValdd

    thetaValdd = - g / r * math.sin(thetaVal)
    thetaVald = thetaVald + thetaValdd * dt
    thetaVal = thetaVal + thetaVald * dt
    print(thetaVal)

    # Update where the hinge is located with reference to window size
    circle.x = window.get_size()[0] / 2
    circle.y = window.get_size()[1] * 5 / 8

    # Update where the arm is located with reference to window size and pendulum angle
    rectangle.x = window.get_size()[0] / 2
    rectangle.y = window.get_size()[1] * 5 / 8
    rectangle.rotation = thetaVal * 180 / math.pi

    # Update where the point mass is located with reference to window size and pendulum angle
    circleTwo.x = window.get_size()[0] / 2 - math.sin(thetaVal) * 200
    circleTwo.y = window.get_size()[1] * 5 / 8 - math.cos(thetaVal) * 200


# Cause the clock update. This is what limits the precious of the simulation (step is is ~1/60)
pyglet.clock.schedule_interval(update, 1/60.0)

# Creates the window
pyglet.app.run()

