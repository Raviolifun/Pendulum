# Standard
import math

# Libraries
from pyglet import shapes

# Application Specific
# (Place Holder)


class MotionFade:
    def __init__(self, x, y, width, size, color1=(255, 255, 255), batch=None, group=None):
        # (x, y) describes the position of the fixed circle
        self._pos = [x, y]

        # size describes the length of the trail ~ in pixels
        self._size = size

        # width describes the width of the trail
        self._width = width

        # Counterclockwise angle from negative vertical (degrees)
        self._rotation = 0

        # Create particle array
        self._particles = [0] * size
        for i in range(size):
            self._particles[i] = shapes.Circle(x=x, y=y, radius=width/2, color=color1, batch=batch, group=group)

    def _update_position(self):
        self._particles.insert(0, self._particles.pop(self._size - 1))
        # Move leading circle
        self._particles[0].x = self._pos[0]
        self._particles[0].y = self._pos[1]
        for i in range(self._size):
            particle = self._particles[i]
            # 0 - 255
            # particle.opacity = i * 255.0 / (self._size - 1)
            particle.opacity = (self._size - 1 - i) * 255.0 / (self._size - 1)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._update_position()
