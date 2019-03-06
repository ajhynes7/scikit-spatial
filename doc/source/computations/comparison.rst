
Comparison
==========


Perpendicularity
----------------

Check if two vectors are perpendicular.

>>> from skspatial.objects import Vector

>>> Vector([0, 1]).is_perpendicular(Vector([1, 0]))
True

>>> Vector([0, -5]).is_perpendicular(Vector([7, 0]))
True

>>> Vector([1, 1]).is_perpendicular(Vector([1, 0]))
False


Parallelism
-----------

Check if two vectors are parallel.

>>> Vector([1, 2, 3]).is_parallel(Vector([2, 4, 6]))
True

>>> Vector([1, 0]).is_parallel(Vector([-1, 0]))
True

>>> Vector([1, 0]).is_parallel(Vector([-1, 5]))
False


Coplanarity
-----------

Check if two lines are coplanar.

>>> from skspatial.objects import Point, Line

>>> line_a = Line(Point([0, 0]), Vector([1, 2]))
>>> line_b = Line(Point([6, 8]), Vector([3, -4]))

>>> line_a.is_coplanar(line_b)
True

>>> line_b = Line(Point([6, 8]), Vector([0, 0, 1]))
>>> line_a.is_coplanar(line_b)
False


Collinearity
------------

Check if three points are collinear.

>>> point_a = Point([0, 0])
>>> point_b = Point([1, 1])
>>> point_c = Point([8, 8])

>>> point_a.is_collinear(point_b, point_c)
True


>>> point_a = Point([-1, 0])
>>> point_a.is_collinear(point_b, point_c)
False
