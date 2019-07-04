
Circle
------

A :class:`~skspatial.objects.Circle` object is defined by a 2D point and a radius. The point is the center of the circle.

>>> from skspatial.objects import Circle

>>> circle = Circle([0, 0], 1)

>>> circle
Circle(point=Point([0, 0]), radius=1)


The circumference and area of the circle can be calculated.

>>> circle.circumference().round(3)
6.283

>>> circle.area().round(3)
3.142


An error is raised if the point is not 2D.

>>> Circle([0, 0, 0], 1)
Traceback (most recent call last):
...
ValueError: The point must be 2D.
