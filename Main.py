# Model for a basic pendulum

# Standard
import math

# Libraries
import pyglet
from pyglet.window import key
from pyglet import shapes

# Application Specific
import Link
import MotionFade
import Graph

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


# For size adjustment
pixelsPerMeter = 100

# Batch of all objects (renders them in one go)
main_batch = pyglet.graphics.Batch()

# Objects to be batched. These create the pendulum seen on the screen
motionFade = MotionFade.MotionFade(x=window.get_size()[0] / 2, y=window.get_size()[1] * 5 / 8 - 200, width=35, size=20,
                                   color1=(40, 105, 215), batch=main_batch)
link = Link.Link(x=window.get_size()[0] / 2, y=window.get_size()[1] * 5 / 8, length=200, color1=(225, 225, 225),
                 color2=(100, 100, 100), color3=(140, 140, 140), batch=main_batch)
graph = Graph.MovingGraph(x=100, y=10, width=200, height=100, colors=((0, 0, 255), (0, 255, 0)), batch=main_batch)

# Function Constants
g = 9.81
r = 4

# Initialisation Constants
thetaVal = 3.1415 + math.pi*2
thetaVald = 1
thetaValdd = 1.5
time = 0


def update(dt):
    # The Dynamic System: x'' * r - g * sin(x) = 0

    # Force these to be global rather than local
    global thetaVal, thetaVald, thetaValdd, time

    # Internal simulation loop for more accurate performance

    dtT = dt
    dtF = 1/500
    while dtT > dtF:
        thetaValdd = - g / r * math.sin(thetaVal)
        # the simple model
        # thetaValdd = - g / r * thetaVal
        thetaVald = thetaVald + thetaValdd * dtF
        thetaVal = thetaVal + thetaVald * dtF
        dtT = dtT - dtF
        # Give graph information, bottom right corner
        #graph.update_graph(time, thetaVal)
        time += dtF

    thetaValdd = - g / r * math.sin(thetaVal)
    # the simple model
    # thetaValdd = - g / r * thetaVal
    thetaVald = thetaVald + thetaValdd * dtT
    thetaVal = thetaVal + thetaVald * dtT
    # Give graph information, bottom right corner
    graph.update_graph(time, (thetaVal + math.pi) % (2 * math.pi) + 2 * math.pi)
    time += dt

    link.x = window.get_size()[0] / 2
    link.y = window.get_size()[1] * 5 / 8
    link.rotation = thetaVal * 180 / math.pi

    # Add a motion Fade to the end of the linkage
    motionFade.pos = [link.x2, link.y2]




# Cause the clock update. This is what limits the precision of the simulation (step is is ~1/60)
pyglet.clock.schedule_interval(update, 1/60.0)

# Creates the window
pyglet.app.run()

