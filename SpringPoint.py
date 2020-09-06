# Planet

import time

from pyglet import shapes


class SpringPoint:

    def __init__(self, x0, y0, vx0, vy0, mass, k, c, n, dispRad=5, color1=(255, 255, 255), batch=None, group=None):
        # Simulation Parameters
        self._x = x0
        self._y = y0
        self._vx = vx0
        self._vy = vy0
        self._ax = 0
        self._ay = 0
        self._mass = mass
        self._k = k
        self._c = c
        self._radius = dispRad
        n = int(n) - 1
        self._neighbors_index = [0]*n
        self._neighborsInitialDis = [0]*n
        self._neighborsCurrentDis = [0]*n


        # Animation Parameters
        self._dispRad = dispRad
        self._color = color1
        self._batch = batch
        self._group = group

        self.circleOne = shapes.Circle(x=x0, y=y0, radius=dispRad, segments=8, color=color1, batch=batch, group=group)

    def updateAccel(self, SpringPoints, Fx, Fy):

        # For code timing
        # tOne = time.perf_counter()
        # tTwo = time.perf_counter()

        total_force_x = 0
        total_force_y = 0

        i = 0
        for value in self._neighbors_index:
            dx = SpringPoints[value].x - self._x
            dy = SpringPoints[value].y - self._y

            self._neighborsCurrentDis[i] = (dx**2 + dy**2)**0.5
            delta_distance = (self._neighborsCurrentDis[i] - self._neighborsInitialDis[i])

            spring_force = self._k * delta_distance
            spring_force = self.non_linear_Spring(self._neighborsInitialDis[i], delta_distance)
            if self._neighborsCurrentDis[i] == 0:
                self._neighborsCurrentDis[i] = 1
            spring_force_x = spring_force * dx / self._neighborsCurrentDis[i]
            spring_force_y = spring_force * dy / self._neighborsCurrentDis[i]

            relative_velocity_x = SpringPoints[value].vx - self._vx
            relative_velocity_y = SpringPoints[value].vy - self._vy
            relative_velocity = (relative_velocity_x**2 + relative_velocity_y**2)**0.5

            damp_force = self._c * relative_velocity
            if relative_velocity == 0:
                relative_velocity = 1
            damp_force_x = damp_force * relative_velocity_x / relative_velocity
            damp_force_y = damp_force * relative_velocity_y / relative_velocity

            total_force_x += damp_force_x + spring_force_x
            total_force_y += damp_force_y + spring_force_y
            i = i + 1

        self._ax = (total_force_x + Fx)/self._mass
        self._ay = (total_force_y + Fy)/self._mass

    def updatePosition(self, stepSize, x_max, y_max):
        self._vx = self._vx + stepSize * self._ax
        self._vy = self._vy + stepSize * self._ay

        x_new = self._x + stepSize * self._vx
        y_new = self._y + stepSize * self._vy

        damp = 0
        friction_damp = 0.8

        if self._x - self._radius < 0:
            x_new = self._radius
            self._vy = friction_damp * self._vy
            self._vx = - damp * self._vx

        if self._x + self._radius > x_max:
            self._vy = friction_damp * self._vy
            x_new = x_max - self._radius
            self._vx = - damp * self._vx

        if self._y - self._radius < 0:
            self._vx = friction_damp * self._vx
            y_new = self._radius
            self._vy = - damp * self._vy

        if self._y + self._radius > y_max:
            self._vx = friction_damp * self._vx
            y_new = y_max - self._radius
            self._vy = - damp * self._vy

        self._x = x_new
        self._y = y_new

    def non_linear_Spring(self, nominal, displacement):
        if displacement + nominal == 0:
            nominal = nominal + 0.1
        return self._k * (displacement/(displacement + nominal) + displacement)


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

    @property
    def neighbors_index(self):
        return self._neighbors_index

    @neighbors_index.setter
    def neighbors_index(self, value):
        self._neighbors_index = value

    @property
    def neighborsInitialDis(self):
        return self._neighborsInitialDis

    @neighborsInitialDis.setter
    def neighborsInitialDis(self, value):
        self._neighborsInitialDis = value
