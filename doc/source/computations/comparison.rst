
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


Collinearity
------------

Check if multiple points are collinear.

>>> from skspatial.objects import Points

>>> Points(([0, 0, 0], [1, 2, 3], [2, 4, 6])).are_collinear()
True

>>> Points(([0, 0, 0], [1, 2, 3], [5, 2, 0])).are_collinear()
False

>>> Points(([0, 0], [1, 2], [5, 2], [6, 3])).are_collinear()
False


Coplanarity
-----------

Check if two lines are coplanar.

>>> from skspatial.objects import Point, Line

>>> line_a = Line(point=[0, 0, 0], direction=[1, 2, 0])
>>> line_b = Line(point=[6, 8, 0], direction=[3, -4, 0])

>>> line_a.is_coplanar(line_b)
True

>>> line_b = Line([6, 8, 0], [0, 0, 1])
>>> line_a.is_coplanar(line_b)
False


