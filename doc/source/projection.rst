
Projection
==========

Point-Line Projection
---------------------

>>> from skspatial.objects import Point, Vector, Line

>>> point = Point([5, 5, 3])
>>> line = Line(Point([0, 0]), Vector([1, 1]))

>>> line.project_point(point)
Point([5. 5. 0.])


Point-Plane Projection
----------------------


Vector Projection
-----------------
