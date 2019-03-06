
Projection
==========


Point-Line Projection
---------------------

Project a point onto a line.

>>> from skspatial.objects import Point, Vector, Line

>>> point = Point([5, 5, 3])
>>> line = Line(Point([0, 0]), Vector([1, 1]))

>>> line.project_point(point)
Point([5. 5. 0.])


Point-Plane Projection
----------------------

Project a point onto a plane.

>>> from skspatial.objects import Plane

>>> point = Point([5, 9, -3])
>>> plane = Plane(Point([0, 0, 0]), Vector([0, 0, 2]))

>>> plane.project_point(point)
Point([5. 9. 0.])


Vector-Vector Projection
------------------------

Project a vector onto a vector.

>>> vector_a = Vector([1, 0])
>>> vector_b = Vector([22, 9])

>>> vector_a.project_vector(vector_b)  # Project vector B onto vector A.
Vector([22.  0.  0.])


Vector-Line Projection
----------------------

Project a vector onto a line.

>>> line = Line(Point([-1, 5, 3]), Vector([3, 4, 5]))
>>> vector = Vector([1, 1, 1])

>>> line.project_vector(vector)
Vector([0.72 0.96 1.2 ])


Vector-Plane Projection
-----------------------

Project a vector onto a plane.

>>> plane = Plane(Point([0, 4]), Vector([0, 1, 1]))
>>> vector = Vector([2, 4, 8])

>>> plane.project_vector(vector)
Vector([ 2. -2.  2.])
