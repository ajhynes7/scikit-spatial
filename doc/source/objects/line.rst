
Line
----

A `Line` is defined by a `Point` and a `Vector`. The direction of the line is the unit vector of the input `Vector`.

>>> from skspatial.objects import Point, Vector, Line

>>> line_1 = Line(Point([0, 0]), Vector([5, 0]))

>>> line_1
Line(point=Point([0. 0. 0.]), direction=Vector([1. 0. 0.]))


The `Point` and `Vector` inputs are not interchangeable.

>>> Line(Vector([0, 0]), Point([5, 0]))
Traceback (most recent call last):
...
dpcontracts.PreconditionError: the types of arguments must be valid


Alternatively, a `Line` can be defined by two points.

>>> line_2 = Line.from_points(Point([0, 0]), Point([100, 0]))

>>> line_1 == line_2
True

The distance from a `Point` to a `Line` can be found.

>>> line_1.distance_point(Point([20, 75]))
75.0

A `Point` can be projected onto a `Line`, returning a new `Point`.

>>> line_1.project_point(Point([50, 20]))
Point([50.  0.  0.])

