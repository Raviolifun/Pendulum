# Planet

import time

from pyglet import shapes

class Planet:

    def __init__(self, x0, y0, vx0, vy0, mass, dispRad=5, color1=(255, 255, 255), batch=None, group=None):
        # Simulation Parameters
        self._x = x0
        self._y = y0
        self._vx = vx0
        self._vy = vy0
        self._ax = 0
        self._ay = 0
        self._mass = mass

        # Animation Parameters
        self._dispRad = dispRad
        self._color = color1
        self._batch = batch
        self._group = group

        self.circleOne = shapes.Circle(x=x0, y=y0, radius=dispRad, segments=8, color=color1, batch=batch, group=group)

    def updateGravAccel(self, planets):

        # For code timing
        # tOne = time.perf_counter()
        # tTwo = time.perf_counter()

        G = 6.67 * 10 ** -11

        axMag = 0
        ayMag = 0

        for planet in planets:

            if planet == self:
                continue
            radius = ((planet.x - self._x)**2 + (planet.y - self._y)**2)**0.5
            if radius < 10**-6:
                radius = 10**-6
            aMag = G*planet.mass/radius**2

            xPort = (planet.x - self._x) / radius
            yPort = (planet.y - self._y) / radius
            axp = aMag * xPort
            ayp = aMag * yPort

            if radius < self._dispRad * 2:
                self._vx = (planet.vx * planet.mass + self._vx * self._mass)/(planet.mass + self._mass)
                self._vy = (planet.vy * planet.mass + self._vy * self._mass)/(planet.mass + self._mass)
                planet.vx = self._vx
                planet.vy = self._vy
                # self._ax = 0
                # self._ay = 0
                # planet._ax = 0
                # planet._ay = 0
            else:
                axMag += axp
                ayMag += ayp

        self._ax = axMag
        self._ay = ayMag

    def updatePosition(self, stepSize):
        self._vx = self._vx + stepSize * self._ax
        self._vy = self._vy + stepSize * self._ay
        self._x = self._x + stepSize * self._vx
        self._y = self._y + stepSize * self._vy

    def updateAnimation(self):
        self.circleOne.x = self._x
        self.circleOne.y = self._y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def vx(self):
        return self._vx

    @vx.setter
    def vx(self, value):
        self._vx = value

    @property
    def vy(self):
        return self._vy

    @vy.setter
    def vy(self, value):
        self._vy = value

    @property
    def ax(self):
        return self._ax

    @ax.setter
    def ax(self, value):
        self._ax = value

    @property
    def ay(self):
        return self._ay

    @ay.setter
    def ay(self, value):
        self._ay = value

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value):
        self._mass = value