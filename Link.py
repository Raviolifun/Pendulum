# Standard
import math

# Libraries
from pyglet import shapes

# Application Specific
# (Place Holder)


class Link:
    def __init__(self, x, y, length, width=0, color1=(255, 255, 255), color2=(200, 200, 200), color3=(200, 200, 200),
                 batch=None, group=None):
        # (x, y) describes the position of the fixed circle
        self._x = x
        self._y = y
        # length describes the length from center to center
        self._length = length
        # Auto scale width with length unless specified
        if width == 0:
            self._width = length/10.0
            width = self._width
        else:
            self._width = width

        # Counterclockwise angle from negative vertical (degrees)
        self._rotation = 0

        # Outline shapes
        # Set up rectangle in center
        self.rectangle = shapes.Rectangle(x=x-width/2, y=y, width=width, height=length,
                                          color=color1, batch=batch, group=group)
        # Anchor rectangle to top middle (allows for rotation about a convenient point)
        self.rectangle._anchor_x = self.rectangle.width / 2
        self.rectangle._anchor_y = self.rectangle.height
        # Set up circles at tips
        self.circleOne = shapes.Circle(x=x, y=y, radius=width/1.1, color=color1, batch=batch, group=group)
        self.circleTwo = shapes.Circle(x=x, y=y+length, radius=width/1.1, color=color1, batch=batch, group=group)

        # Inner shapes
        # Set up rectangle in center
        self.rectangleIn = shapes.Rectangle(x=x-width*0.3125, y=y, width=width*0.625, height=length,
                                            color=color3, batch=batch, group=group)
        # Anchor rectangle to top middle (allows for rotation about a convenient point)
        self.rectangleIn._anchor_x = self.rectangleIn.width / 2
        self.rectangleIn._anchor_y = self.rectangleIn.height
        # Set up circles at tips
        self.circleOneIn = shapes.Circle(x=x, y=y, radius=width*0.833/1.1, color=color2, batch=batch, group=group)
        self.circleTwoIn = shapes.Circle(x=x, y=y+length, radius=width*0.833/1.1, color=color2, batch=batch, group=group)

    def _update_position(self):
        # Updates position of outer
        # Move fixed circle
        self.circleOne.x = self._x
        self.circleOne.y = self._y
        # Move moving circle (linkage end)
        self.circleTwo.x = self._x + math.sin(self._rotation * math.pi / 180) * self._length
        self.circleTwo.y = self._y - math.cos(self._rotation * math.pi / 180) * self._length
        # Rotate rectangle
        self.rectangle.x = self._x
        self.rectangle.y = self._y
        self.rectangle.rotation = -self._rotation

        # Updates position of inner
        # Move fixed circle
        self.circleOneIn.x = self._x
        self.circleOneIn.y = self._y
        # Move moving circle (linkage end)
        self.circleTwoIn.x = self._x + math.sin(self._rotation * math.pi / 180) * self._length
        self.circleTwoIn.y = self._y - math.cos(self._rotation * math.pi / 180) * self._length
        # Rotate rectangle
        self.rectangleIn.x = self._x
        self.rectangleIn.y = self._y
        self.rectangleIn.rotation = -self._rotation

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

    @property
    def x2(self):
        """X coordinate of the shape.

        :type: int or float
        """
        return self._x + math.sin(self._rotation * math.pi / 180) * self._length

    @property
    def y2(self):
        """Y coordinate of the shape.

        :type: int or float
        """
        return self._y - math.cos(self._rotation * math.pi / 180) * self._length

