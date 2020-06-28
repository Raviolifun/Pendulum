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
window = pyglet.window.Window(900, 700, caption='Simulation of Pendulum', resizable=True)
window.set_minimum_size(320, 200)
window.set_maximum_size(1920, 1080)
icon1 = pyglet.image.load('.\\resources\\Bee.png')
icon2 = pyglet.image.load('.\\resources\\Bee32.png')
window.set_icon(icon1, icon2)
fps_display = pyglet.window.FPSDisplay(window=window)


# Required for updating the screen
@window.event
def on_draw():
    window.clear()
    main_batch.draw()
    # fps_display.draw()


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
motionFade = MotionFade.MotionFade(x=window.get_size()[0] / 2, y=window.get_size()[1] * 5 / 8 - 200, width=35, size=200,
                                   color1=(40, 105, 215), batch=main_batch)
motionFade2 = MotionFade.MotionFade(x=window.get_size()[0] / 2, y=window.get_size()[1] * 5 / 8 - 200, width=35, size=200,
                                   color1=(40, 105, 215), batch=main_batch)
link = Link.Link(x=window.get_size()[0] / 2, y=window.get_size()[1] * 4 / 8, length=200, color1=(225, 225, 225),
                 color2=(100, 100, 100), color3=(140, 140, 140), batch=main_batch)
link2 = Link.Link(x=window.get_size()[0] / 2, y=window.get_size()[1] * 4 / 8, length=200, color1=(225, 225, 225),
                 color2=(100, 100, 100), color3=(140, 140, 140), batch=main_batch)
# graph = Graph.MovingGraph(x=100, y=10, width=200, height=100, colors=((0, 0, 255), (0, 255, 0)), batch=main_batch)

# Function Constants
g = 9.81
r1 = 2
m1 = 4
r2 = 2
m2 = 4

# Initialisation Constants
th = math.pi
thd = 0
thdd = 0
ps = 0
psd = 0
psdd = 0
time = 0


def update(dt):
    # The Dynamic System: is a double pendulum

    # Force these to be global rather than local
    global th, thd, thdd, ps, psd, psdd, time

    # Internal simulation loop for more accurate performance

    dtT = dt
    dtF = 1/10000
    while dtT > dtF:
        # The system is gaining energy significantly
        # when ps or th is large it seems to hurt worst
        # I would bet on th... but who knows
        # when m2 is 0 the system behaves as expected for a degenerate double pendulum
        # when ps is near pi/2 it seems to diverge faster? could be wrong though

        numer = - m1 * g * math.sin(th) + math.sin(ps) * m2 * (g * math.cos(th + ps) + (thd**2) * r1 * math.cos(ps) + ((thd + psd)**2) * r2)
        thdd = numer/(r1 * m1 + r1 * m2 * (math.sin(ps)**2))
        psdd = (-thdd * r1 * math.cos(ps) - (thd**2) * r1 * math.sin(ps) - thdd * r2 - math.sin(th + ps) * g) / r2

        thd = thd + thdd * dtF
        th = th + thd * dtF
        psd = psd + psdd * dtF
        ps = ps + psd * dtF

        dtT = dtT - dtF
        # Give graph information, bottom right corner
        time += dtF

    numer = - m1 * g * math.sin(th) + math.sin(ps) * m2 * (g * math.cos(th + ps) + (thd ** 2) * r1 * math.cos(ps) + ((thd + psd) ** 2) * r2)
    thdd = numer / (r1 * m1 + r1 * m2 * (math.sin(ps) ** 2))
    psdd = (-thdd * r1 * math.cos(ps) - (thd ** 2) * r1 * math.sin(ps) - thdd * r2 - math.sin(th + ps) * g) / r2

    thd = thd + thdd * dtT
    th = th + thd * dtT
    psd = psd + psdd * dtT
    ps = ps + psd * dtT

    # graph.update_graph(time, thd + 4)
    # graph.update_graph(time, psd + 4)
    time += dt

    link.x = window.get_size()[0] / 2
    link.y = window.get_size()[1] * 4 / 8
    link.rotation = th * 180 / math.pi
    link2.x = link.x2
    link2.y = link.y2
    link2.rotation = (ps + th) * 180 / math.pi

    # Add a motion Fade to the end of the linkage
    motionFade.pos = [link.x2, link.y2]
    motionFade2.pos = [link2.x2, link2.y2]

    enr = ((thd * r1)**2 * m1 + (-thd * r1 - (thd + psd)*r2)**2 * m2) * 1/2.0 \
          - m1 * g * math.cos(th)*r1 - m2 * g * (math.cos(th)*r1 + math.cos(th + ps)*r2)
    # graph.update_graph(time, enr/1000.0 + 8)
    print(enr)

# Cause the clock update. This is what limits the precision of the simulation (step is is ~1/60)
pyglet.clock.schedule_interval(update, 1/60.0)

# Creates the window
pyglet.app.run()

