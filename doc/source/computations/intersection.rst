
Intersection
============

Line-Line intersection
----------------------

The intersection of a :class:`~skspatial.objects.Line` with a :class:`~skspatial.objects.Line` is a :class:`~skspatial.objects.Point`.

>>> from skspatial.objects import Line

>>> line_a = Line(point=[0, 0], direction=[1, 1])
>>> line_b = Line([10, 0], [0, 1])

>>> line_a.intersect_line(line_b)
Point([10., 10.])


In order to intersect, the lines must be coplanar and not parallel. An error is returned otherwise.

>>> line_a = Line([0, 0, 0], [1, 0, 0])
>>> line_b = Line([0, 1, 0], [1, 1, 1])

>>> line_a.intersect_line(line_b)
Traceback (most recent call last):
...
ValueError: The lines must be coplanar.

>>> line_b = Line([0, 1, 0], [5, 0, 0])
>>> line_a.intersect_line(line_b)
Traceback (most recent call last):
...
ValueError: The lines must not be parallel.



Line-Plane intersection
-----------------------

The intersection of a :class:`~skspatial.objects.Line` with a :class:`~skspatial.objects.Plane` is a :class:`~skspatial.objects.Point`.

>>> from skspatial.objects import Plane

>>> line = Line([5, 5, 3], [0, 0, -1])
>>> plane = Plane([0, 0, 0], [0, 0, 1])

>>> plane.intersect_line(line)
Point([5., 5., 0.])


The line must not be parallel to the plane.

>>> line = Line([5, 5, 3], [0, 1, 0])
>>> plane.intersect_line(line)
Traceback (most recent call last):
...
ValueError: The line and plane must not be parallel.



Plane-Plane intersection
------------------------

The intersection of a :class:`~skspatial.objects.Plane` with a :class:`~skspatial.objects.Plane` is a :class:`~skspatial.objects.Line`.

>>> plane_a = Plane([0, 0, 0], [-1, 1, 0])
>>> plane_b = Plane([8, 0, 0], [1, 1, 0])

>>> plane_a.intersect_plane(plane_b)
Line(point=Point([4., 4., 0.]), direction=Vector([ 0,  0, -2]))


The planes must not be parallel.

>>> plane_b = Plane([8, 0, 0], [-1, 1, 0])
>>> plane_a.intersect_plane(plane_b)
Traceback (most recent call last):
...
ValueError: The planes must not be parallel.
