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
import Graph

# Setup for limiting the window size, adding icons, and adding an FPS display
window = pyglet.window.Window(900, 700, caption='Simulation of Pendulum', resizable=True)
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
motionFade = MotionFade.MotionFade(x=window.get_size()[0] / 2, y=window.get_size()[1] * 5 / 8 - 200, width=35, size=20,
                                   color1=(40, 105, 215), batch=main_batch)
link = Link.Link(x=window.get_size()[0] / 2, y=window.get_size()[1] * 4 / 8, length=200, color1=(225, 225, 225),
                 color2=(100, 100, 100), color3=(140, 140, 140), batch=main_batch)
# linka = Link.Link(x=window.get_size()[0] / 2, y=window.get_size()[1] * 4 / 8, length=200, color1=(225, 225, 225),
#                  color2=(100, 100, 100), color3=(140, 140, 140), batch=main_batch)
graph = Graph.MovingGraph(x=100, y=10, width=200, height=100, colors=((0, 0, 255), (0, 255, 0)), batch=main_batch)

# Function Constants
g = 9.81
l0 = 10
m = 0.1
k = 1000000
p = 1.225
A = 0.01
cd = 0.47

# Initialisation Constants
th = math.pi/2+0.0000001
thd = 0
thdd = 0
xx = 0
xxd = 0
xxdd = 0

xPosf = xPos
yPosf = yPos
vxf = 0
vyf = 0

vx = 0
vy = 0
ax = 0
ay = 0
vxr = 0
vyr = 0
time = 0


def update(dt):
    # The Dynamic System: is a double pendulum

    # Force these to be global rather than local
    global th, thd, thdd, xx, xxd, xxdd, vxr, vyr, time
    global xPosf, xPos, yPosf, yPos, vxf, vx, vyf, vy, ax, ay

    dtT = dt
    dtF = 1/10000
    while dtT > dtF:

        vyy = -vy + thd * (l0 + xx) * math.sin(th) + vyr - xxd * math.cos(th)
        vxx = -vx + thd * (l0 + xx) * math.cos(th) + vxr + xxd * math.sin(th)
        ps = -math.atan2(vyy, vxx)
        VV2 = vxx ** 2 + vyy ** 2
        R2 = 1 / 2.0 * p * A * cd * VV2

        thdd = (m * g * math.sin(th) + m * thd * xxd + R2 * math.cos(ps + th) + m * ax * math.cos(
            th) + m * ay * math.sin(th)) / -(l0 * m + xx * m)
        xxdd = (m * thd ** 2 * (xx + l0) + m * g * math.cos(th) - k * xx - R2 * math.sin(ps + th) - m * ax * math.sin(
            th) + m * ay * math.cos(th)) / m

        thd = thd + thdd * dtF
        th = th + thd * dtF
        xxd = xxd + xxdd * dtF
        xx = xx + xxd * dtF

        dtT = dtT - dtF
        # Give graph information, bottom right corner
        time += dtF

    vyy = -vy + thd * (l0 + xx) * math.sin(th) + vyr - xxd * math.cos(th)
    vxx = -vx + thd * (l0 + xx) * math.cos(th) + vxr + xxd * math.sin(th)
    ps = -math.atan2(vyy, vxx)
    VV2 = vxx ** 2 + vyy ** 2
    R2 = 1 / 2.0 * p * A * cd * VV2

    thdd = (m * g * math.sin(th) + m * thd * xxd + R2 * math.cos(ps + th) + m * ax * math.cos(
        th) + m * ay * math.sin(th)) / -(l0 * m + xx * m)
    xxdd = (m * thd ** 2 * (xx + l0) + m * g * math.cos(th) - k * xx - R2 * math.sin(ps + th) - m * ax * math.sin(
        th) + m * ay * math.cos(th)) / m

    thd = thd + thdd * dtF
    th = th + thd * dtF
    xxd = xxd + xxdd * dtF
    xx = xx + xxd * dtF

    # This is for the mouse interaction code
    vx = (xPosf - xPos)/(pixelsPerMeter * dt)
    vy = (yPosf - yPos)/(pixelsPerMeter * dt)
    ax = (vxf - vx)/dt
    ay = (vyf - vy)/dt

    graph.update_graph(time, thd/4 + 4)
    graph.update_graph(time, xxd/4 + 4)
    time += dt

    # for mouse velocity calcs
    xPosf = xPos
    yPosf = yPos
    vxf = vx
    vyf = vy

    # on resize:
    # link.x = window.get_size()[0] / 2
    # link.y = window.get_size()[1] * 4 / 8
    # else:
    link.x = xPos
    link.y = yPos

    link.rotation = th * 180 / math.pi
    link.length = pixelsPerMeter * (l0 + xx)

    # linka.x = link.x2
    # linka.y = link.y2
    # linka.rotation = (-ps) * 180 / math.pi + 90

    # Add a motion Fade to the end of the linkage
    motionFade.pos = [link.x2, link.y2]


# Cause the clock update. This is what limits the precision of the simulation (step is is ~1/60)
pyglet.clock.schedule_interval(update, 1/60.0)

# Creates the window
pyglet.app.run()

