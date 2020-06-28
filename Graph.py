# This code allows the creation of a graph
# Desired features:
# Auto rescaling
# Initial width and height
# x and y scale
# different colors for each input
# any numerical input (table or individual values)
# Any x? default to over time?
# Maybe labels in the long term
# Standard
import math

# Libraries
from pyglet import shapes

# Application Specific
# (Place Holder)


class MovingGraph:
    def __init__(self, x, y, width, height, colors, backColor=(255, 255, 255), xMax=1, xMin=-1, yMax=1, yMin=-1,
                 batch=None, group=None):

        # Boarder
        self._borderWidth = 2

        # describes the position of the bottom left corner
        self._x = x
        self._y = y

        # size of graph
        self._width = width
        self._height = height
        self._insideWidth = width - 2 * self._borderWidth
        self._insideHeight = height - 2 * self._borderWidth

        # number of saved points
        self._n = 1

        # colors for each line
        self._colors = colors

        # x and y Range
        self._xMax = xMax
        self._xMin = xMin
        self._yMax = yMax
        self._yMin = yMin

        # x and y Scale, Scales values into pixels
        self._xScale = self._insideWidth / (xMax - xMin)
        self._yScale = self._insideHeight / (yMax - yMin)

        # Past X Value
        self._xPast = 0

        # Batch and Group
        self._batch = batch
        self._group = group

        """
        # Boarder
        self._rectangleBorder = shapes.Rectangle(x=x, y=y, width=width, height=height, color=(100, 100, 100),
                                                 batch=batch, group=group)
        # GraphWindow
        self._rectangleInside = shapes.Rectangle(x=x + self._borderWidth, y=y + self._borderWidth, width=width - 2 * self._borderWidth,
                                                 height=height - 2 * self._borderWidth, color=backColor, batch=batch,
                                                 group=group)
        # x-Axis
        self._xAxis = shapes.Line(x=x + self._borderWidth, y=y + self._borderWidth + 5, x2=x + self._borderWidth + self._insideWidth,
                                  y2=y + self._borderWidth + 5, color=(0, 0, 0), batch=batch, group=group)
        # y-Axis
        self._yAxis = shapes.Line(x=x + self._borderWidth + 5, y=y + self._borderWidth, x2=x + self._borderWidth + 5,
                                  y2=y + self._borderWidth + self._insideHeight, color=(0, 0, 0), batch=batch, group=group)
                                  """
        # inputPoints
        # Doing this with circles. The code would be faster if individual points were used
        self._points = [[]]
        for j in range(len(colors)):
            self._points[0].append(shapes.Circle(x=self._x + self._width - self._borderWidth, y=y, segments=4,
                                                 radius=4, color=colors[j], batch=batch, group=group))

    def update_graph(self, x, y):
        # Given new position data, update list

        # Auto y resize
        if y * self._yScale > self._y + self._height - self._borderWidth:
            self._yMax = y
        elif y * self._yScale < self._y + self._borderWidth:
            self._yMin = y
        else:
            a = 1
            #self._points[self._n - 1][j].y = y * self._yScale

        dx = (x - self._xPast) * self._xScale

        # if x pos is less than back edge
        # remove point
        # if x pos is equal to or greater than back edge
        # add point

        if self._points[0][0].x < self._x + self._borderWidth:
            # If there are too many points lengthwise
            self._points.pop(0)
            self._n = self._n - 1

            # Shift all the points over by dx and move point from back to front
            self._points.insert(self._n - 1, self._points.pop(0))
            for j in range(len(self._colors)):
                self._points[self._n - 1][j].x = self._x + self._width - self._borderWidth
                self._points[self._n - 1][j].y = y * self._yScale
            for i in range(self._n):
                for j in range(len(self._colors)):
                    self._points[i][j].x = self._points[i][j].x - dx
        else:
            # If there are not enough points lengthwise
            self._points.append([])
            for j in range(len(self._colors)):
                self._points[self._n].append(shapes.Circle(x=self._x + self._width - self._borderWidth,
                                                           y=y * self._yScale, segments=4, radius=4,
                                                           color=self._colors[j], batch=self._batch, group=self._group))
            self._n = self._n + 1
            # Shift all the points over by dx
            for i in range(self._n):
                for j in range(len(self._colors)):
                    self._points[i][j].x = self._points[i][j].x - dx

        self._xPast = x
