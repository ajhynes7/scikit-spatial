
Intersection
============

Line-Line intersection
----------------------

The intersection of a `Line` with a `Line` is a `Point`.

>>> from skspatial.objects import Point, Vector, Line

>>> line_a = Line(Point([0, 0]), Vector([1, 1]))
>>> line_b = Line(Point([10, 0]), Vector([0, 1]))

>>> line_a.intersect_line(line_b)
Point([10. 10.  0.])


In order to intersect, the lines must be coplanar and not parallel. An error is returned otherwise.

>>> line_b = Line(Point([10, 0]), Vector([1, 1, 1]))
>>> line_a.intersect_line(line_b)
Traceback (most recent call last):
...
dpcontracts.PreconditionError: The lines must be coplanar.

>>> line_b = Line(Point([10, 0]), Vector([1, 1]))
>>> line_a.intersect_line(line_b)
Traceback (most recent call last):
...
dpcontracts.PreconditionError: The lines must not be parallel.



Line-Plane intersection
-----------------------

The intersection of a `Line` with a `Plane` is a `Point`.

>>> from skspatial.objects import Plane

>>> line = Line(Point([5, 5, 3]), Vector([0, 0, -1]))
>>> plane = Plane(Point([0, 0, 0]), Vector([0, 0, 1]))

>>> plane.intersect_line(line)
Point([5. 5. 0.])


The line must not be parallel to the plane.

>>> line = Line(Point([5, 5, 3]), Vector([0, 1, 0]))
>>> plane.intersect_line(line)
Traceback (most recent call last):
...
dpcontracts.PreconditionError: The line and plane must not be parallel.



Plane-Plane intersection
------------------------

The intersection of a `Plane` with a `Plane` is a `Line`.

>>> plane_a = Plane(Point([0, 0, 0]), Vector([-1, 1, 0]))
>>> plane_b = Plane(Point([8, 0, 0]), Vector([1, 1, 0]))

>>> plane_a.intersect_plane(plane_b)
Line(point=Point([4. 4. 0.]), direction=Vector([ 0.  0. -1.]))


The planes must not be parallel.

>>> plane_b = Plane(Point([8, 0, 0]), Vector([-1, 1, 0]))
>>> plane_a.intersect_plane(plane_b)
Traceback (most recent call last):
...
dpcontracts.PreconditionError: The planes must not be parallel.
