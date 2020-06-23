# Standard
import math

# Libraries
from pyglet import shapes

# Application Specific
# (Place Holder)


class Link:
    def __init__(self, x, y, length, color1=(255, 255, 255), color2=(200, 200, 200), color3=(200, 200, 200), batch=None, group=None):
        self._x = x
        self._y = y
        self._length = length
        # Angle from negative vertical (degrees)
        self._rotation = 0

        # Outline
        self.rectangle = shapes.Rectangle(x=x-length/20, y=y, width=length/10, height=length,
                                          color=color1, batch=batch, group=group)
        self.rectangle._anchor_x = self.rectangle.width / 2
        self.rectangle._anchor_y = self.rectangle.height
        self.circleOne = shapes.Circle(x=x, y=y, radius=length/10, color=color1, batch=batch, group=group)
        self.circleTwo = shapes.Circle(x=x, y=y+length, radius=length/10, color=color1, batch=batch, group=group)

        # Inner
        self.rectangleIn = shapes.Rectangle(x=x-length/32, y=y, width=length/16, height=length,
                                            color=color3, batch=batch, group=group)
        self.rectangleIn._anchor_x = self.rectangleIn.width / 2
        self.rectangleIn._anchor_y = self.rectangleIn.height
        self.circleOneIn = shapes.Circle(x=x, y=y, radius=length/12, color=color2, batch=batch, group=group)
        self.circleTwoIn = shapes.Circle(x=x, y=y+length, radius=length/12, color=color2, batch=batch, group=group)

    def _update_position(self):
        self.circleOne.x = self._x
        self.circleOne.y = self._y
        self.circleTwo.x = self._x - math.sin(self._rotation * math.pi / 180) * self._length
        self.circleTwo.y = self._y - math.cos(self._rotation * math.pi / 180) * self._length
        self.rectangle.x = self._x
        self.rectangle.y = self._y
        self.rectangle.rotation = self._rotation

        self.circleOneIn.x = self._x
        self.circleOneIn.y = self._y
        self.circleTwoIn.x = self._x - math.sin(self._rotation * math.pi / 180) * self._length
        self.circleTwoIn.y = self._y - math.cos(self._rotation * math.pi / 180) * self._length
        self.rectangleIn.x = self._x
        self.rectangleIn.y = self._y
        self.rectangleIn.rotation = self._rotation

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        self._length = length
        self._update_position()

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = rotation
        self._update_position()

    @property
    def x(self):
        """X coordinate of the shape.

        :type: int or float
        """
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._update_position()

    @property
    def y(self):
        """Y coordinate of the shape.

        :type: int or float
        """
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._update_position()
