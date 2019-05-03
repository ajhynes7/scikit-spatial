
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


Concurrency
------------

Check if multiple points are concurrent.

>>> from skspatial.objects import Points

>>> Points([[0, 0], [1, 1], [1, 1]]).are_concurrent()
False

>>> Points([[1, 1], [1, 1], [1, 1]]).are_concurrent()
True


Collinearity
------------

Check if multiple points are collinear.

>>> Points(([0, 0, 0], [1, 2, 3], [2, 4, 6])).are_collinear()
True

>>> Points(([0, 0, 0], [1, 2, 3], [5, 2, 0])).are_collinear()
False

>>> Points(([0, 0], [1, 2], [5, 2], [6, 3])).are_collinear()
False


Coplanarity
-----------

Check if multiple points are coplanar.

>>> Points([[1, 2], [9, -18], [12, 4], [2, 1]]).are_coplanar()
True


Check if two lines are coplanar.

>>> from skspatial.objects import Point, Line

>>> line_a = Line(point=[0, 0, 0], direction=[1, 2, 0])
>>> line_b = Line(point=[6, 8, 0], direction=[3, -4, 0])

>>> line_a.is_coplanar(line_b)
True

>>> line_b = Line([6, 8, 0], [0, 0, 1])
>>> line_a.is_coplanar(line_b)
False


Vector-Vector Side
------------------

Find the side of a target vector where another vector is directed.
Both vectors must be 2D.


>>> vector_target = Vector([0, 1])


The vector is parallel to the target vector. 

>>> vector_target.side_vector([0, 2])
0
>>> vector_target.side_vector([0, -5])
0


The vector is to the right of the target vector.

>>> vector_target.side_vector([1, 1])
1
>>> vector_target.side_vector([1, -10])
1


The vector is to the left of the target vector.

>>> vector_target.side_vector([-3, 4])
-1


Point-Line Side
---------------

Find the side of the line where a point lies.
The line and point must be 2D.


>>> line = Line([0, 0], [1, 1])


The point is on the line.

>>> line.side_point([2, 2])
0


The point is to the right of the line.

>>> line.side_point([5, 3])
1


The point is to the left of the line.

>>> line.side_point([5, 10])
-1


Point-Plane Side
----------------

Find the side of the plane where a point lies.


>>> from skspatial.objects import Plane
>>> plane = Plane([0, 0, 0], [0, 0, 1])


The point is in on the plane.

>>> plane.side_point([2, 5, 0])
0


The point is in front of the plane.

>>> plane.side_point([1, -5, 6])
1


The point is behind the plane.

>>> plane.side_point([5, 8, -4])
-1


Higher dimensions are supported.

>>> plane = Plane([0, 0, 0, 0], [0, 1, 0, 1])

>>> plane.side_point([0, -10, 4, 1])
-1
