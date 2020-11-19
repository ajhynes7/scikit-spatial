
Line
----

A :class:`~skspatial.objects.Line` object is defined by a point and a direction vector.

>>> from skspatial.objects import Line

>>> line_1 = Line(point=[0, 0], direction=[5, 0])

>>> line_1
Line(point=Point([0, 0]), direction=Vector([5, 0]))


Alternatively, a line can be defined by two points.

>>> line_2 = Line.from_points([0, 0], [100, 0])

>>> line_1.is_close(line_2)
True


The ``is_close`` method checks if two lines are equal within a tolerance.

Lines with different points and directions can still be equal. One line must contain the other line's point, and their vectors must be parallel.

>>> line_1 = Line([0, 0], [1, 0])
>>> line_2 = Line([10, 0], [-5, 0])

>>> line_1.is_close(line_2)
True

The distance from a point to a line can be found.

>>> line_1.distance_point([20, 75])
75.0

A point can be projected onto a line, returning a new :class:`~skspatial.objects.Point` object.

>>> line_1.project_point([50, 20])
Point([50.,  0.])

