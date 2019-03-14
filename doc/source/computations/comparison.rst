
Comparison
==========


Perpendicularity
----------------

Check if two vectors are perpendicular.

>>> from skspatial.objects import Vector

>>> Vector([0, 1]).is_perpendicular([1, 0])
True

>>> Vector([0, -5]).is_perpendicular([7, 0])
True

>>> Vector([1, 1]).is_perpendicular([1, 0])
False


Parallelism
-----------

Check if two vectors are parallel.

>>> Vector([1, 2, 3]).is_parallel([2, 4, 6])
True

>>> Vector([1, 0]).is_parallel([-1, 0])
True

>>> Vector([1, 0]).is_parallel([-1, 5])
False


Coplanarity
-----------

Check if two lines are coplanar.

>>> from skspatial.objects import Point, Line

>>> line_a = Line(point=[0, 0], vector=[1, 2])
>>> line_b = Line(point=[6, 8], vector=[3, -4])

>>> line_a.is_coplanar(line_b)
True

>>> line_b = Line([6, 8], [0, 0, 1])
>>> line_a.is_coplanar(line_b)
False


Collinearity
------------

Check if three points are collinear.

>>> Point([0, 0]).is_collinear([1, 1], [8, 8])
True

>>> Point([-1, 0]).is_collinear([1, 1], [8, 8])
False
